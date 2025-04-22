from rest_framework import serializers
from core.models import Produto, Plataforma, Grupo

class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = ['id', 'nome']

class ProdutoSerializer(serializers.ModelSerializer):
    plataforma_nome = serializers.ReadOnlyField(source='plataforma.nome')
    
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'concorrente', 'url', 'plataforma', 
            'plataforma_nome', 'grupo', 'data_criacao', 
            'ultima_verificacao', 'posicao_fila', 'verificacao_manual'
        ]
        read_only_fields = ['data_criacao', 'ultima_verificacao']

class ProdutoDetalheSerializer(ProdutoSerializer):
    class Meta(ProdutoSerializer.Meta):
        depth = 1