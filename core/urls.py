from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ClienteViewSet, ProdutoViewSet, HistoricoPrecoViewSet
from core.views.auth_views import get_user_info, change_password

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'historico', HistoricoPrecoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # URLs para autenticação
    path('user/info/', get_user_info, name='user_info'),
    path('user/change-password/', change_password, name='change_password'),
]