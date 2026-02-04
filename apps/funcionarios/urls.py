# apps/funcionarios/urls.py
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from .views import FuncionarioViewSet, HorarioTrabalhoViewSet

router = DefaultRouter()
router.register('horarios', HorarioTrabalhoViewSet, basename='horario-trabalho')
=======
from .views import FuncionarioViewSet

router = DefaultRouter()
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
router.register('', FuncionarioViewSet, basename='funcionario')

urlpatterns = router.urls

