from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ClienteViewSet, ProdutoViewSet, HistoricoPrecoViewSet
from core.views.auth_views import get_user_info, change_password, set_cliente_atual
from core.views.produto_views import ProdutoViewSet
from core.views.cliente_views import ClienteViewSet
from core.views.historico_views import HistoricoPrecoViewSet
from core.views.plataforma_views import PlataformaViewSet
from core.views.grupo_views import GrupoViewSet


router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'historico', HistoricoPrecoViewSet)
router.register(r'plataformas', PlataformaViewSet)
router.register(r'grupos', GrupoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # URLs para autenticação
    path('user/info/', get_user_info, name='user_info'),
    path('user/change-password/', change_password, name='change_password'),
    path('user/set-cliente/', set_cliente_atual, name='set_cliente_atual'),
]