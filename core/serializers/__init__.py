from .cliente_serializers import ClienteSerializer
from .produto_serializers import ProdutoSerializer, ProdutoDetalheSerializer, PlataformaSerializer
from .historico_serializers import HistoricoPrecoSerializer, HistoricoPrecoResumoSerializer
from .grupo_serializers import GrupoSerializer

__all__ = [
    'ClienteSerializer',
    'ProdutoSerializer',
    'ProdutoDetalheSerializer',
    'PlataformaSerializer',
    'HistoricoPrecoSerializer',
    'HistoricoPrecoResumoSerializer',
    'GrupoSerializer',
]