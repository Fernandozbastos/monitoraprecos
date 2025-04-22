from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from core.models import HistoricoPreco, Produto
from core.serializers import HistoricoPrecoSerializer

class HistoricoPrecoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricoPreco.objects.all()
    serializer_class = HistoricoPrecoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produto', 'data']
    
    def get_queryset(self):
        user = self.request.user
        # Se não for admin, filtra por cliente atual
        if user.tipo != 'admin' and user.cliente_atual:
            return self.queryset.filter(produto__cliente=user.cliente_atual)
        return self.queryset