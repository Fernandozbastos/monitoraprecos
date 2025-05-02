from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Produto, HistoricoPreco
from core.serializers import ProdutoSerializer, ProdutoDetalheSerializer, HistoricoPrecoResumoSerializer
from django.utils import timezone
import logging
from django.db import transaction

# Configurar logger
logger = logging.getLogger(__name__)

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'plataforma', 'verificacao_manual', 'grupo', 'tipo_produto', 'produto_cliente']
    search_fields = ['nome', 'concorrente', 'url']
    ordering_fields = ['nome', 'data_criacao', 'ultima_verificacao']
    ordering = ['-data_criacao']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProdutoDetalheSerializer
        return self.serializer_class
    
    def get_queryset(self):
        user = self.request.user
        # Se não for admin, filtra por cliente atual
        if user.tipo != 'admin' and user.cliente_atual:
            return self.queryset.filter(cliente=user.cliente_atual)
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Criando produto com dados: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro ao criar produto: {str(e)}")
            raise
    
    def partial_update(self, request, *args, **kwargs):
        """
        Sobrescreve o método partial_update para lidar com atualizações parciais,
        especialmente para o campo produto_cliente.
        """
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
        
        # Se estiver atualizando o campo produto_cliente para True
        if 'produto_cliente' in request.data and request.data['produto_cliente']:
            try:
                with transaction.atomic():
                    # Desmarcar outros produtos com o mesmo nome
                    Produto.objects.filter(
                        cliente=instance.cliente,
                        nome=instance.nome,
                        produto_cliente=True
                    ).exclude(id=instance.id).update(produto_cliente=False)
                    
                    # Atualizar apenas o campo produto_cliente
                    instance.produto_cliente = True
                    instance.save(update_fields=['produto_cliente'])
                    
                    # Retornar o produto atualizado
                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)
                    
            except Exception as e:
                logger.error(f"Erro ao atualizar status de produto cliente: {str(e)}")
                return Response(
                    {"detail": f"Erro ao atualizar: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    def partial_update(self, request, *args, **kwargs):
        """
        Sobrescreve o método partial_update para lidar com atualizações parciais,
        incluindo a mudança de produto para tipo cliente quando marcado como produto_cliente.
        """
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
        print(f"Dados recebidos no PATCH: {request.data}")
        
        # Se estiver atualizando para produto_cliente=True e o tipo for concorrente
        if request.data.get('produto_cliente') is True and instance.tipo_produto == 'concorrente':
            # Garantir que o tipo seja alterado para 'cliente'
            if 'tipo_produto' not in request.data:
                request.data['tipo_produto'] = 'cliente'
                print(f"Alterando automaticamente o tipo para 'cliente'. Dados atualizados: {request.data}")
        
        # Para atualizações parciais, usar o comportamento padrão
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        produto = self.get_object()
        historico = HistoricoPreco.objects.filter(produto=produto).order_by('-data')[:30]
        serializer = HistoricoPrecoResumoSerializer(historico, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verificar(self, request, pk=None):
        """Endpoint para verificar o preço de um produto manualmente."""
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
    
    @action(detail=True, methods=['post'])
    def atualizar_preco_cliente(self, request, pk=None):
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
            
        except Exception as e:
            return Response(
                {"detail": f"Erro ao atualizar preço: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )