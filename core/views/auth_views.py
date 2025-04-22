from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Usuario
from core.serializers.usuario_serializers import UsuarioSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """Endpoint para obter informações do usuário logado"""
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Endpoint para alterar a senha do usuário"""
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    # Verificar se a senha atual está correta
    if not user.check_password(current_password):
        return Response({'detail': 'Senha atual incorreta'}, status=400)
    
    # Alterar a senha
    user.set_password(new_password)
    user.save()
    return Response({'detail': 'Senha alterada com sucesso'})