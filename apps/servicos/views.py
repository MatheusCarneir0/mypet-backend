# apps/servicos/views.py
"""
Views para gerenciamento de serviços.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Servico
from .serializers import (
    ServicoSerializer,
    ServicoListSerializer,
    ServicoCreateUpdateSerializer
)
<<<<<<< HEAD
from apps.core.permissions import IsAdministrador
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
from apps.swagger.servicos import servico_view_schema


@servico_view_schema
class ServicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações de Serviço.
<<<<<<< HEAD
    - list/retrieve: qualquer usuário autenticado
    - create/update/delete: apenas administrador
    """
    queryset = Servico.objects.filter(ativo=True)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdministrador()]
=======
    """
    queryset = Servico.objects.filter(ativo=True)
    permission_classes = [IsAuthenticated]
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServicoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ServicoCreateUpdateSerializer
        return ServicoSerializer
