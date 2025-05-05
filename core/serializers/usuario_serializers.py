from rest_framework import serializers
from core.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    # Garantir que cliente_atual sempre retorne o ID e não o objeto
    cliente_atual = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # Adicionar campos personalizados para retornar dados básicos do cliente atual
    cliente_atual_nome = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'tipo', 'cliente_atual', 'cliente_atual_nome']
        read_only_fields = ['date_joined']
        extra_kwargs = {'password': {'write_only': True}}
        
    def get_cliente_atual_nome(self, obj):
        """Retorna o nome do cliente atual se existir"""
        if obj.cliente_atual:
            return obj.cliente_atual.nome
        return None
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user