# apps/authentication/urls.py
"""
URLs para autenticação.
<<<<<<< HEAD
Agrupa: Login (JWT), Registro de Clientes e Refresh Token.
=======
Agrupa: Login (JWT), Registro de Clientes, Google Login e Refresh Token.
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
"""
from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    RegistroView,
<<<<<<< HEAD
    PasswordResetRequestView,
    PasswordResetConfirmView,
=======
    GoogleLoginView,
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
)

app_name = 'authentication'

urlpatterns = [
    # Autenticação JWT
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
<<<<<<< HEAD

    # Registro de Clientes
    path('register/', RegistroView.as_view(), name='register'),

    # Recuperação de Senha
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
=======
    
    # Registro de Clientes
    path('register/', RegistroView.as_view(), name='register'),
    
    # Login Social
    path('google/', GoogleLoginView.as_view(), name='google'),
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
]

