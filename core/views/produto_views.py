from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Produto, HistoricoPreco
from core.serializers import ProdutoSerializer, ProdutoDetalheSerializer, HistoricoPrecoResumoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'plataforma', 'verificacao_manual', 'grupo']
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