from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Produto, HistoricoPreco
from core.serializers import ProdutoSerializer, ProdutoDetalheSerializer, HistoricoPrecoResumoSerializer
from django.utils import timezone
import logging

# Configurar logger
logger = logging.getLogger(__name__)

class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de produtos.
    Fornece operações CRUD completas para produtos e endpoints adicionais
    para verificação de preços e histórico.
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'plataforma', 'verificacao_manual', 'grupo', 'tipo_produto', 'produto_cliente']
    search_fields = ['nome', 'concorrente', 'url']
    ordering_fields = ['nome', 'data_criacao', 'ultima_verificacao']
    ordering = ['-data_criacao']
    
    def get_serializer_class(self):
        """Determina qual serializer usar com base na ação."""
        if self.action == 'retrieve':
            return ProdutoDetalheSerializer
        return self.serializer_class
    
    def get_queryset(self):
        """
        Filtra os produtos com base no usuário atual.
        Se não for admin, mostra apenas produtos do cliente atual.
        """
        user = self.request.user
        # Se não for admin, filtra por cliente atual
        if user.tipo != 'admin' and user.cliente_atual:
            return self.queryset.filter(cliente=user.cliente_atual)
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        """
        Cria um novo produto com logs detalhados para depuração.
        """
        logger.info(f"Criando produto com dados: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro ao criar produto: {str(e)}")
            raise
    
    def partial_update(self, request, *args, **kwargs):
        """
        Sobrescreve o método partial_update para lidar com atualizações parciais,
        incluindo a mudança de produto para tipo cliente quando marcado como produto_cliente.
        Implementação sem usar transaction.
        """
        try:
            instance = self.get_object()
            
            # Verificar se o usuário tem um cliente atual definido
            user = request.user
            if not user.cliente_atual:
                return Response(
                    {"detail": "Você precisa selecionar um cliente atual antes de realizar esta operação."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Verificar se o produto pertence ao cliente atual do usuário
            if instance.cliente.id != user.cliente_atual.id:
                return Response(
                    {"detail": "Este produto não pertence ao cliente atual selecionado."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Log para depuração
            logger.info(f"Dados recebidos no PATCH: {request.data}")
            
            # Fazer uma cópia mutável dos dados recebidos
            data = request.data.copy()

            # Adicione o cliente e grupo aos dados se não estiverem presentes
            if 'cliente' not in data:
                data['cliente'] = instance.cliente.id

            if 'grupo' not in data:
                data['grupo'] = instance.grupo.id
            
            # Se estiver atualizando para produto_cliente=True
            if data.get('produto_cliente') is True:
                # Desmarcar outros produtos com o mesmo nome e do mesmo cliente
                outros_produtos = Produto.objects.filter(
                    cliente=instance.cliente,
                    nome=instance.nome,
                    produto_cliente=True
                ).exclude(id=instance.id)
                
                # Atualiza cada produto individualmente
                for p in outros_produtos:
                    p.produto_cliente = False
                    p.save()
                
                # Se o tipo for concorrente, alterar para cliente
                if instance.tipo_produto == 'concorrente':
                    if 'tipo_produto' not in data:
                        data['tipo_produto'] = 'cliente'
                        logger.info(
                            "Alterando automaticamente o tipo para 'cliente'. Dados atualizados: %s",
                            data,
                        )
            # Para atualizações parciais, utilizar a mesma lógica do mixin
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)
        
        except Exception as e:
            logger.error(f"Erro ao atualizar produto: {str(e)}")
            return Response(
                {"detail": f"Erro ao atualizar: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """
        Endpoint para recuperar o histórico de preços de um produto.
        Retorna os últimos 30 registros por padrão.
        """
        produto = self.get_object()
        
        # Verificar se o usuário tem acesso ao produto
        user = request.user
        if user.tipo != 'admin' and user.cliente_atual and produto.cliente.id != user.cliente_atual.id:
            return Response(
                {"detail": "Você não tem permissão para acessar o histórico deste produto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Parâmetros de filtro
        limit = request.query_params.get('limit', 30)
        try:
            limit = int(limit)
        except ValueError:
            limit = 30
        
        # Limite máximo para evitar sobrecarga
        if limit > 100:
            limit = 100
        
        historico = HistoricoPreco.objects.filter(produto=produto).order_by('-data')[:limit]
        serializer = HistoricoPrecoResumoSerializer(historico, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verificar(self, request, pk=None):
        """
        Endpoint para verificar o preço de um produto manualmente.
        Agenda uma tarefa assíncrona para fazer o scraping.
        """
        from scraper.tasks import verificar_preco
        
        produto = self.get_object()
        
        # Verificar se o usuário tem um cliente atual definido
        user = request.user
        if not user.cliente_atual:
            return Response(
                {"detail": "Você precisa selecionar um cliente atual antes de realizar esta operação."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Verificar se o produto pertence ao cliente atual do usuário
        if produto.cliente.id != user.cliente_atual.id:
            return Response(
                {"detail": "Este produto não pertence ao cliente atual selecionado."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Agenda a tarefa de verificação de preço
        task = verificar_preco.delay(produto.id)
        
        return Response({
            'message': f'Verificação de preço agendada para {produto.nome}',
            'task_id': task.id
        })
    
    @action(detail=False, methods=['post'])
    def verificar_todos(self, request):
        """
        Endpoint para verificar todos os produtos do cliente atual.
        Agenda tarefas assíncronas para lotes de produtos.
        """
        from scraper.tasks import verificar_todos_produtos
        
        # Verificar se o usuário tem um cliente atual definido
        user = request.user
        if not user.cliente_atual:
            return Response(
                {"detail": "Você precisa selecionar um cliente atual antes de realizar esta operação."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obter os produtos do cliente atual
        produtos = Produto.objects.filter(cliente=user.cliente_atual)
        
        if not produtos.exists():
            return Response(
                {"detail": "Não há produtos para verificar."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parâmetros para controlar o tamanho dos lotes
        tamanho_lote = request.data.get('tamanho_lote', 20)
        try:
            tamanho_lote = int(tamanho_lote)
            if tamanho_lote <= 0:
                tamanho_lote = 20
        except (ValueError, TypeError):
            tamanho_lote = 20
        
        # Limitar o número máximo de produtos para evitar sobrecarga
        max_produtos = request.data.get('max_produtos', produtos.count())
        try:
            max_produtos = int(max_produtos)
            if max_produtos <= 0:
                max_produtos = produtos.count()
        except (ValueError, TypeError):
            max_produtos = produtos.count()
        
        # Agendar a verificação de todos os produtos
        task = verificar_todos_produtos.delay(tamanho_lote, max_produtos)
        
        return Response({
            'message': f'Verificação agendada para {min(max_produtos, produtos.count())} produtos',
            'task_id': task.id
        })
    
    @action(detail=True, methods=['post'])
    def atualizar_preco_cliente(self, request, pk=None):
        """
        Endpoint para atualizar manualmente o preço de um produto do cliente.
        Também atualiza o histórico de preços.
        """
        produto = self.get_object()
        
        # Verificar se o usuário tem um cliente atual definido
        user = request.user
        if not user.cliente_atual:
            return Response(
                {"detail": "Você precisa selecionar um cliente atual antes de realizar esta operação."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Verificar se o produto pertence ao cliente atual do usuário
        if produto.cliente.id != user.cliente_atual.id:
            return Response(
                {"detail": "Este produto não pertence ao cliente atual selecionado."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verifica se é um produto do cliente
        if produto.tipo_produto != 'cliente':
            return Response(
                {"detail": "Este endpoint só pode ser usado para produtos do cliente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtém o preço do request
        preco = request.data.get('preco_cliente')
        if preco is None:
            return Response(
                {"detail": "O preço do cliente é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Converte para float se for string
            if isinstance(preco, str):
                preco = float(preco.replace(',', '.'))
            
            # Validação básica
            if preco <= 0:
                return Response(
                    {"detail": "O preço deve ser maior que zero."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Atualiza o preço
            produto.preco_cliente = preco
            produto.save(update_fields=['preco_cliente'])
            
            # Atualiza o histórico
            HistoricoPreco.objects.create(
                produto=produto,
                preco=preco
            )
            
            # Atualiza a última verificação
            produto.ultima_verificacao = timezone.now()
            produto.save(update_fields=['ultima_verificacao'])
            
            # Serializa e retorna o produto atualizado
            serializer = self.get_serializer(produto)
            return Response(serializer.data)
            
        except ValueError:
            return Response(
                {"detail": "Formato de preço inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Erro ao atualizar preço do cliente: {str(e)}")
            return Response(
                {"detail": f"Erro ao atualizar preço: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )