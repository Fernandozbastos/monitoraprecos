from rest_framework import viewsets, permissions
from core.models import Grupo
from core.serializers import GrupoSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [permissions.IsAuthenticated]