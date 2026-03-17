<<<<<<< HEAD
"""
URL configuration for MyPet Backend project.
=======
# config/urls.py
"""
URLs principais do projeto MyPet.
Organização: Admin Django, Documentação, API Routes.
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # API v1
    path('api/v1/', include('config.api_urls')),
    
    path('health/', include('core.urls')),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

=======
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # Raiz da API — retorna JSON de boas-vindas
    path('', api_root, name='api-root'),
    # Django Admin (painel administrativo nativo)
    path('django-admin/', admin.site.urls),
    
    # API Documentation (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Routes - Autenticação e Perfil
    path('auth/', include('apps.authentication.urls')),  # Login, Registro, Google, Refresh
    path('me/', include('apps.me.urls')),  # Perfil do usuário autenticado
    
    # API Routes - Gestão de Clientes e Pets
    path('clientes/', include('apps.clientes.urls')),  # CRUD Clientes (apenas Funcionário/Admin listam)
    path('pets/', include('apps.pets.urls')),  # CRUD Pets (filtro automático por tipo de usuário)
    
    # API Routes - Agendamentos e Serviços
    path('agendamentos/', include('apps.agendamentos.urls')),  # Agendamentos (apenas ações POST)
    path('servicos/', include('apps.servicos.urls')),  # Serviços disponíveis
    
    # API Routes - Pagamentos e Notificações
    path('pagamentos/', include('apps.pagamentos.urls')),
    path('notificacoes/', include('apps.notificacoes.urls')),  # Notificações do usuário
    
    # API Routes - Histórico
    path('historico/', include('apps.historico.urls')),  # Histórico de atendimentos
    
    # API Routes - Administração (Apenas Admin)
    path('admin/', include('apps.admin.urls')),  # Dashboard, Relatórios, Funcionários, Formas de Pagamento
    
    # API Routes - Funcionários
    path('funcionarios/', include('apps.funcionarios.urls')),
]

# Media files em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug Toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
