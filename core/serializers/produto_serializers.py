from rest_framework import serializers
from core.models import Produto, Plataforma, Grupo

class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = ['id', 'nome']

class ProdutoSerializer(serializers.ModelSerializer):
    plataforma_nome = serializers.ReadOnlyField(source='plataforma.nome')
    menor_preco_concorrente = serializers.SerializerMethodField()
    diferenca_percentual = serializers.SerializerMethodField()
    status_preco = serializers.SerializerMethodField()
    
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'tipo_produto', 'preco_cliente', 'menor_preco_concorrente',
            'diferenca_percentual', 'status_preco', 'plataforma', 'plataforma_nome',
            'ultima_verificacao', 'url', 'concorrente', 'grupo', 'verificacao_manual'
        ]
        read_only_fields = ['data_criacao', 'ultima_verificacao']

    def get_menor_preco_concorrente(self, obj):
        menor_preco = obj.get_menor_preco_concorrente()
        return round(menor_preco, 2) if menor_preco else None

    def get_diferenca_percentual(self, obj):
        return obj.calcular_diferenca_percentual()
        
    def get_status_preco(self, obj):
        """Retorna o status do preço: 'melhor', 'pior' ou None."""
        diferenca = obj.calcular_diferenca_percentual()
        if diferenca is None:
            return None
        return 'melhor' if diferenca <= 0 else 'pior'

class ProdutoDetalheSerializer(ProdutoSerializer):
    class Meta(ProdutoSerializer.Meta):
        depth = 1