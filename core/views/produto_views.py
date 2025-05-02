from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Produto, HistoricoPreco
from core.serializers import ProdutoSerializer, ProdutoDetalheSerializer, HistoricoPrecoResumoSerializer
from django.utils import timezone

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'plataforma', 'verificacao_manual', 'grupo', 'tipo_produto']
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
    
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        produto = self.get_object()
        historico = HistoricoPreco.objects.filter(produto=produto).order_by('-data')[:30]
        serializer = HistoricoPrecoResumoSerializer(historico, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def atualizar_preco_cliente(self, request, pk=None):
        produto = self.get_object()
        
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