from .cliente_views import ClienteViewSet
from .produto_views import ProdutoViewSet
from .historico_views import HistoricoPrecoViewSet
from .plataforma_views import PlataformaViewSet
from .grupo_views import GrupoViewSet

__all__ = [
    'ClienteViewSet',
    'ProdutoViewSet',
    'HistoricoPrecoViewSet',
    'PlataformaViewSet',
    'GrupoViewSet',
]