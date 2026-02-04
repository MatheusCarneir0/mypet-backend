# apps/pets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
=======
from rest_framework_nested import routers
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
from .views import PetViewSet

router = DefaultRouter()
router.register('', PetViewSet, basename='pet')

urlpatterns = [
    path('', include(router.urls)),
<<<<<<< HEAD
=======
    # Rota manual para o histórico sem precisar da lib nested
    path('<int:pet_pk>/historico/', PetViewSet.as_view({'get': 'historico'}), name='pet-historico'),
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
]