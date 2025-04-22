from rest_framework import viewsets, permissions
from core.models import Cliente
from core.serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['nome']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_criacao']
    ordering = ['nome']