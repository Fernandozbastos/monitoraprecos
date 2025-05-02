from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Usuario, Cliente
from core.serializers.usuario_serializers import UsuarioSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """Endpoint para obter informações do usuário logado"""
    user = request.user
    # Garantir que cliente_atual seja um ID, não um objeto
    if hasattr(user, 'cliente_atual') and user.cliente_atual:
        # Log para verificar o tipo do cliente_atual
        print(f"Tipo do cliente_atual: {type(user.cliente_atual)}")
        print(f"Valor do cliente_atual: {user.cliente_atual}")
    
    serializer = UsuarioSerializer(user)
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_cliente_atual(request):
    """Endpoint para definir o cliente atual do usuário"""
    cliente_id = request.data.get('cliente_atual')
    
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return Response({'detail': 'Cliente não encontrado'}, status=400)
    
    # Atualiza o cliente atual do usuário
    user = request.user
    user.cliente_atual = cliente
    user.save()
    
    # Retorna os dados atualizados do usuário
    serializer = UsuarioSerializer(user)
    return Response(serializer.data)