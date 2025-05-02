# Arquivo: core/serializers/produto_serializers.py

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
            'id', 'nome', 'tipo_produto', 'preco_cliente', 'produto_cliente',
            'menor_preco_concorrente', 'diferenca_percentual', 'status_preco', 
            'plataforma', 'plataforma_nome', 'ultima_verificacao', 'url', 
            'concorrente', 'grupo', 'verificacao_manual', 'cliente'
        ]
        read_only_fields = ['data_criacao', 'ultima_verificacao']

    def validate(self, data):
        """
        Validação personalizada que verifica se os campos obrigatórios estão presentes
        apenas em operações de criação ou atualização completa, não em atualizações parciais.
        """
        # Obter o método da requisição
        # Se não houver request context (por exemplo, em serialização), ignore a validação
        request = self.context.get('request')
        if not request:
            return data

        # Para operações PATCH (atualização parcial) e GET, não validar campos obrigatórios
        if request.method in ['PATCH', 'GET']:
            return data
            
        # Para outros métodos (POST, PUT), validar campos obrigatórios
        if not data.get('cliente'):
            raise serializers.ValidationError({"cliente": "O cliente é obrigatório."})
        if not data.get('grupo'):
            raise serializers.ValidationError({"grupo": "O grupo é obrigatório."})
            
        return data
        
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

# Adicione a classe ProdutoDetalheSerializer que estava faltando
class ProdutoDetalheSerializer(ProdutoSerializer):
    """
    Serializer com mais detalhes para o produto.
    Estende ProdutoSerializer e adiciona mais profundidade na serialização.
    """
    class Meta(ProdutoSerializer.Meta):
        depth = 1  # Aumenta a profundidade da serialização para mostrar objetos relacionados