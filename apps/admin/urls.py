# apps/admin/urls.py
"""
URLs para rotas administrativas.
<<<<<<< HEAD
Agrupa dashboard, relatórios e formas de pagamento.
=======
Agrupa dashboard, relatórios, funcionários e formas de pagamento.
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DashboardView, RelatorioGerarView
<<<<<<< HEAD
from .views import AdminFormaPagamentoViewSet

app_name = 'backoffice'

# Router para ViewSets
router = DefaultRouter()
=======
from apps.funcionarios.views import FuncionarioViewSet
from .views import AdminFormaPagamentoViewSet

app_name = 'backoffice'

# Router para ViewSets
router = DefaultRouter()
router.register('funcionarios', FuncionarioViewSet, basename='admin-funcionario')
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
router.register('formas-pagamento', AdminFormaPagamentoViewSet, basename='admin-forma-pagamento')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('relatorios/gerar/', RelatorioGerarView.as_view(), name='relatorios-gerar'),
    path('', include(router.urls)),
]

