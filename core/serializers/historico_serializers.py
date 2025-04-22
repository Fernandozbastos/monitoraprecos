from rest_framework import serializers
from core.models import HistoricoPreco

class HistoricoPrecoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    
    class Meta:
        model = HistoricoPreco
        fields = ['id', 'produto', 'produto_nome', 'preco', 'data']
        read_only_fields = ['data']

# Adicione esta classe que está faltando
class HistoricoPrecoResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoPreco
        fields = ['preco', 'data']