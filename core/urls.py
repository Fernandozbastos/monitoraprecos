from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    cliente_views, 
    produto_views, 
    historico_views, 
    auth_views,
    dashboard_views
)

router = DefaultRouter()
# Registrar viewsets aqui quando estiverem implementados
# router.register(r'clientes', cliente_views.ClienteViewSet)
# router.register(r'produtos', produto_views.ProdutoViewSet)
# router.register(r'historico', historico_views.HistoricoPrecoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Adicionar rotas específicas aqui
    # path('auth/login/', auth_views.login_view, name='login'),
    # path('dashboard/', dashboard_views.dashboard_view, name='dashboard'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ClienteViewSet, ProdutoViewSet, HistoricoPrecoViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'historico', HistoricoPrecoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]