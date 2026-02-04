# apps/agendamentos/views.py
"""
Views para gerenciamento de agendamentos.
"""
<<<<<<< HEAD
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action

logger = logging.getLogger(__name__)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils import timezone
from datetime import datetime
=======
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils import timezone
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
from .models import Agendamento
from .serializers import (
    AgendamentoSerializer,
    AgendamentoListSerializer,
    AgendamentoCreateSerializer,
    AgendamentoDetailSerializer,
<<<<<<< HEAD
    AgendamentoUpdateSerializer,
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    ConcluirAgendamentoSerializer,
)
from .services import AgendamentoService
from .filters import AgendamentoFilter
from apps.swagger.agendamentos import agendamento_view_schema
<<<<<<< HEAD
from apps.core.permissions import IsAdministrador, IsFuncionario, IsCliente, IsOwnerOrFuncionario, IsCargoMatchesService
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


@agendamento_view_schema
class AgendamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações de Agendamento.
    SEGURANÇA CRÍTICA: Bloqueia métodos PUT, PATCH e DELETE genéricos.
    As alterações de estado devem ser Ações de Negócio (POST).
<<<<<<< HEAD
    
    Permissões:
    - Admin: Pode criar, editar, cancelar qualquer agendamento
    - Funcionário: Pode criar, listar agendamentos
    - Cliente: Pode criar e gerenciar seus próprios agendamentos
    """
    queryset = Agendamento.objects.all().select_related(
        'cliente', 'pet', 'servico', 'funcionario', 'forma_pagamento'
=======
    """
    queryset = Agendamento.objects.all().select_related(
        'cliente', 'pet', 'servico', 'funcionario'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AgendamentoFilter
    ordering_fields = ['data_hora', 'status']
    ordering = ['-data_hora']
<<<<<<< HEAD
    
    def get_serializer_class(self):
        """Retorna serializer apropriado para a ação."""
        if self.action == 'create':
            return AgendamentoCreateSerializer
        elif self.action == 'retrieve':
            return AgendamentoDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return AgendamentoUpdateSerializer
        elif self.action == 'list':
            return AgendamentoListSerializer
        return AgendamentoSerializer

    def get_queryset(self):
        """
        Filtra agendamentos baseado no tipo de usuário.
        - Admin: vê todos
        - Funcionário: vê todos
        - Cliente: vê apenas seus
        """
        user = self.request.user
        queryset = Agendamento.objects.all().select_related(
            'cliente', 'pet', 'servico', 'funcionario', 'forma_pagamento'
        )

        if user.is_administrador:
            # Admin vê todos
            return queryset
        elif user.is_funcionario:
            # Funcionário vê apenas os que ele é responsável
            return queryset.filter(funcionario__usuario=user)
        elif user.is_cliente:
            # Cliente vê apenas seus agendamentos
            return queryset.filter(cliente__usuario=user)
        return queryset.none()

    def perform_create(self, serializer):
        """
        Cria agendamento.
        - Cliente: cria para si mesmo
        - Admin/Funcionário: pode especificar cliente via cliente_id
        """
        user = self.request.user
        
        if user.is_cliente or user.is_administrador or user.is_funcionario:
            serializer.save()
        else:
            raise PermissionDenied("Você não tem permissão para criar agendamentos.")

    def perform_update(self, serializer):
        """Atualiza agendamento."""
        user = self.request.user
        obj = self.get_object()
        
        # Apenas Admin, Funcionário ou o próprio cliente podem atualizar
        if user.is_administrador or user.is_funcionario or obj.cliente.usuario == user:
            serializer.save()
        else:
            raise PermissionDenied("Você não tem permissão para atualizar este agendamento.")

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrFuncionario])
    def cancelar(self, request, pk=None):
        """Cancela um agendamento."""
        agendamento = self.get_object()
        
        if not agendamento.pode_cancelar:
            return Response(
                {'erro': 'Este agendamento não pode ser cancelado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        agendamento.status = Agendamento.Status.CANCELADO
        agendamento.save()
        
        return Response(
            AgendamentoDetailSerializer(agendamento).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrFuncionario])
    def reagendar(self, request, pk=None):
        """Reagenda um agendamento para nova data/hora."""
        agendamento = self.get_object()
        nova_data_hora_str = request.data.get('data_hora')
        forma_pagamento_id = request.data.get('forma_pagamento_id')
        
        if not nova_data_hora_str:
            return Response(
                {'erro': 'Campo data_hora é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.utils.dateparse import parse_datetime
            nova_data_hora = parse_datetime(nova_data_hora_str)
            if nova_data_hora is None:
                nova_data_hora = datetime.fromisoformat(nova_data_hora_str.replace('Z', '+00:00'))
            if not timezone.is_aware(nova_data_hora):
                nova_data_hora = timezone.make_aware(nova_data_hora)
        except (ValueError, TypeError):
            return Response(
                {'erro': 'Formato de data/hora inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        force = request.user.is_administrador or request.user.is_superuser
        agendamento = AgendamentoService.reagendar(agendamento, nova_data_hora, forma_pagamento_id=forma_pagamento_id, force=force)
        return Response(
            AgendamentoDetailSerializer(agendamento).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsFuncionario, IsCargoMatchesService])
    def iniciar(self, request, pk=None):
        """Inicia o atendimento de um agendamento."""
        agendamento = self.get_object()
        
        if not agendamento.pode_iniciar:
            return Response(
                {'erro': 'Este agendamento não pode ser iniciado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        agendamento.status = Agendamento.Status.EM_ANDAMENTO
        agendamento.save()
        
        return Response(
            AgendamentoDetailSerializer(agendamento).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsFuncionario, IsCargoMatchesService])
    def concluir(self, request, pk=None):
        """Conclui um agendamento."""
        agendamento = self.get_object()
        
        if not agendamento.pode_concluir:
            return Response(
                {'erro': 'Este agendamento não pode ser concluído.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ConcluirAgendamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        agendamento = AgendamentoService.concluir_agendamento(
            agendamento,
            observacoes=serializer.validated_data.get('observacoes', ''),
            valor_pago=serializer.validated_data.get('valor_pago'),
            forma_pagamento_id=serializer.validated_data.get('forma_pagamento_id'),
        )
        
        return Response(
            AgendamentoDetailSerializer(agendamento).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def disponibilidade(self, request):
        """
        Retorna horários disponíveis para uma data e serviço.
        
        Parâmetros:
        - data: YYYY-MM-DD (obrigatório)
        - servico_id: ID do serviço (obrigatório)
        - pet_id: ID do pet (opcional, para calcular duração por porte)
        
        Retorna:
        {
            "data": "2026-03-15",
            "servico_id": 1,
            "horarios": [
                {"hora": "14:00", "data_hora": "2026-03-15T14:00:00Z", "disponivel": true},
                ...
            ]
        }
        """
        data_str = request.query_params.get('data')
        servico_id = request.query_params.get('servico_id')
        pet_id = request.query_params.get('pet_id')
        
        if not data_str or not servico_id:
            return Response(
                {'erro': 'Parâmetros data e servico_id são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'erro': 'Formato de data inválido. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pet_id_int = int(pet_id) if pet_id else None
            horarios = AgendamentoService.horarios_disponiveis(data, int(servico_id), pet_id=pet_id_int)
            return Response({
                'data': data_str,
                'servico_id': servico_id,
                'horarios': horarios
            })
        except ValidationError as e:
            return Response(
                {'erro': e.detail if hasattr(e, 'detail') else 'Dados inválidos.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            logger.exception('Erro ao buscar horários disponíveis')
            return Response(
                {'erro': 'Erro interno ao buscar horários. Tente novamente.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        """Bloqueia PUT genérico, permite PATCH para administradores."""
        if not kwargs.get('partial', False):
            return Response(
                {'erro': 'Use as ações específicas (cancelar, iniciar, concluir)'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        if not (request.user.is_administrador or request.user.is_superuser):
            return Response(
                {'erro': 'Use as ações específicas (cancelar, iniciar, concluir)'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Permite PATCH apenas para administradores."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Bloqueia DELETE genérico."""
        return Response(
            {'erro': 'Use a ação cancelar ao invés de deletar'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
=======
    # Bloquear PUT, PATCH e DELETE - apenas GET e POST permitidos
    http_method_names = ['get', 'post', 'head', 'options']
    
    def get_serializer_class(self):
        """
        Serializers por ação.
        """
        if self.action == 'list':
            return AgendamentoListSerializer
        elif self.action == 'create':
            return AgendamentoCreateSerializer
        elif self.action == 'retrieve':
            return AgendamentoDetailSerializer
        return AgendamentoSerializer
    
    def get_permissions(self):
        """
        Permissões por ação.
        """
        if self.action in ['cancelar', 'reagendar']:
            # Cliente pode cancelar/reagendar seus próprios agendamentos
            from apps.core.permissions import IsOwnerOrAdmin
            return [IsOwnerOrAdmin()]
        elif self.action in ['iniciar', 'concluir']:
            # Apenas funcionário pode iniciar/concluir
            from apps.core.permissions import IsFuncionario
            return [IsFuncionario()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        Filtrar agendamentos baseado no tipo de usuário.
        """
        user = self.request.user
        queryset = super().get_queryset()
        
        # Cliente vê apenas seus agendamentos
        if user.is_cliente:
            try:
                return queryset.filter(cliente__usuario=user)
            except:
                return queryset.none()
        
        # Funcionário vê agendamentos atribuídos a ele
        elif user.is_funcionario:
            try:
                return queryset.filter(funcionario__usuario=user)
            except:
                return queryset.none()
        
        # Administrador vê todos
        return queryset
    
    def perform_create(self, serializer):
        """
        Criar agendamento via service.
        """
        try:
            cliente = self.request.user.cliente
            agendamento = AgendamentoService.criar_agendamento(
                cliente=cliente,
                pet_id=serializer.validated_data['pet'].id,
                servico_id=serializer.validated_data['servico'].id,
                data_hora=serializer.validated_data['data_hora'],
                forma_pagamento_id=serializer.validated_data['forma_pagamento'].id,
                observacoes=serializer.validated_data.get('observacoes', '')
            )
            # Atribuir o agendamento criado ao serializer para retornar
            serializer.instance = agendamento
        except Exception as e:
            from rest_framework import serializers as drf_serializers
            raise drf_serializers.ValidationError({'error': str(e)})
    
    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        """
        POST /agendamentos/{id}/cancelar/
        Cancela um agendamento. Exigir motivo no corpo (UC07).
        """
        agendamento = self.get_object()
        motivo = request.data.get('motivo', '')
        
        if not motivo:
            return Response({
                'error': 'Campo "motivo" é obrigatório para cancelamento.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            AgendamentoService.cancelar_agendamento(agendamento, motivo)
            return Response({
                'message': 'Agendamento cancelado com sucesso.',
                'agendamento': AgendamentoDetailSerializer(agendamento).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='reagendar')
    def reagendar(self, request, pk=None):
        """
        POST /agendamentos/{id}/reagendar/
        Reagenda um agendamento. Validar nova data_hora via AgendamentoService (UC08).
        """
        agendamento = self.get_object()
        nova_data_hora = request.data.get('data_hora')
        
        if not nova_data_hora:
            return Response({
                'error': 'Campo "data_hora" é obrigatório.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from datetime import datetime
            if isinstance(nova_data_hora, str):
                nova_data_hora = timezone.datetime.fromisoformat(nova_data_hora.replace('Z', '+00:00'))
            
            AgendamentoService.reagendar(agendamento, nova_data_hora)
            return Response({
                'message': 'Agendamento reagendado com sucesso.',
                'agendamento': AgendamentoDetailSerializer(agendamento).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='iniciar')
    def iniciar(self, request, pk=None):
        """
        POST /agendamentos/{id}/iniciar/
        Inicia um agendamento. Alterar status para EM_ANDAMENTO (Apenas funcionário).
        """
        agendamento = self.get_object()
        
        try:
            funcionario = request.user.funcionario
            AgendamentoService.iniciar_agendamento(agendamento, funcionario)
            return Response({
                'message': 'Agendamento iniciado.',
                'agendamento': AgendamentoDetailSerializer(agendamento).data
            }, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({
                'error': 'Apenas funcionários podem iniciar agendamentos.'
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='concluir')
    def concluir(self, request, pk=None):
        """
        POST /agendamentos/{id}/concluir/
        Finaliza serviço, captura observacoes, registra pagamento e 
        gera entrada no HistoricoAtendimento (UC15).
        """
        agendamento = self.get_object()
        serializer = ConcluirAgendamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            valor_pago = serializer.validated_data.get('valor_pago')
            observacoes = serializer.validated_data.get('observacoes', '')
            
            AgendamentoService.concluir_agendamento(
                agendamento,
                observacoes=observacoes,
                valor_pago=valor_pago
            )
            return Response({
                'message': 'Agendamento concluído. Histórico registrado.',
                'agendamento': AgendamentoDetailSerializer(agendamento).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='disponibilidade')
    def disponibilidade(self, request):
        """
        GET /agendamentos/disponibilidade/
        Query params: data e servico_id para retornar horários livres (UC06).
        """
        data_str = request.query_params.get('data')
        servico_id = request.query_params.get('servico_id')
        
        if not data_str or not servico_id:
            return Response({
                'error': 'Parâmetros "data" e "servico_id" são obrigatórios.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from datetime import datetime
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
            horarios = AgendamentoService.horarios_disponiveis(data_obj, int(servico_id))
            return Response({
                'data': data_str,
                'servico_id': int(servico_id),
                'horarios': horarios
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({
                'error': f'Formato de data inválido. Use YYYY-MM-DD. Erro: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
