from rest_framework import serializers
from core.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    # Adicionar campo explícito para cliente_atual para garantir que seja o ID
    cliente_atual = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'tipo', 'cliente_atual']
        read_only_fields = ['date_joined']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user