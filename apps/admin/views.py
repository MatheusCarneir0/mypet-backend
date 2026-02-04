# apps/admin/views.py
"""
Views administrativas para dashboard e relatórios.
"""
<<<<<<< HEAD
import logging
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
<<<<<<< HEAD

logger = logging.getLogger(__name__)
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
from apps.core.permissions import IsAdministrador
from apps.relatorios.services import RelatorioService
from apps.relatorios.serializers import RelatorioSerializer, RelatorioCreateSerializer
from apps.pagamentos.models import FormaPagamento
from apps.pagamentos.serializers import FormaPagamentoSerializer
from apps.swagger.admin import (
    dashboard,
    gerar_relatorio,
    admin_forma_pagamento_view_schema
)


@dashboard
class DashboardView(APIView):
    """
    View para dashboard administrativo.
    Retorna métricas gerenciais.
    """
    permission_classes = [IsAuthenticated, IsAdministrador]
    
    def get(self, request):
        """
        Retorna dados para dashboard gerencial.
        """
        try:
            data = RelatorioService.obter_dashboard_data()
            return Response(data, status=status.HTTP_200_OK)
<<<<<<< HEAD
        except Exception:
            logger.exception('Erro ao obter dados do dashboard')
            return Response({
                'error': 'Erro interno ao carregar dashboard. Tente novamente.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
=======
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


@gerar_relatorio
class RelatorioGerarView(APIView):
    """
    View para gerar relatórios administrativos.
    """
    permission_classes = [IsAuthenticated, IsAdministrador]
    
    def post(self, request):
        """
        Gera um novo relatório.
        """
        serializer = RelatorioCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            relatorio = RelatorioService.gerar_relatorio(
                administrador=request.user,
                tipo=serializer.validated_data['tipo'],
                formato=serializer.validated_data['formato'],
                filtros=dict(serializer.validated_data)
            )
            
            return Response(
                RelatorioSerializer(relatorio).data,
                status=status.HTTP_201_CREATED
            )
<<<<<<< HEAD
        except Exception:
            logger.exception('Erro ao gerar relatório')
            return Response({
                'error': 'Erro interno ao gerar relatório. Tente novamente.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
=======
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


@admin_forma_pagamento_view_schema
class AdminFormaPagamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet administrativo para formas de pagamento (CRUD completo).
    """
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]

