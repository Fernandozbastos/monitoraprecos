from rest_framework import viewsets, permissions
from core.models import Plataforma
from core.serializers import PlataformaSerializer

class PlataformaViewSet(viewsets.ModelViewSet):
    queryset = Plataforma.objects.all()
    serializer_class = PlataformaSerializer
    permission_classes = [permissions.IsAuthenticated]