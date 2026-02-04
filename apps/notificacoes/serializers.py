# apps/notificacoes/serializers.py
"""
Serializers para o app de notificações.
"""
from rest_framework import serializers
from .models import Notificacao


class NotificacaoSerializer(serializers.ModelSerializer):
    """
    Serializer de Notificação.
    """
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )
    canal_display = serializers.CharField(
        source='get_canal_display',
        read_only=True
    )
    
    class Meta:
        model = Notificacao
        fields = [
            'id', 'agendamento', 'tipo', 'tipo_display',
<<<<<<< HEAD
            'canal', 'canal_display',
            'assunto', 'mensagem', 'enviada', 'data_envio',
            'data_criacao'
        ]
        read_only_fields = ['id', 'data_criacao']


class NotificacaoAdminSerializer(serializers.ModelSerializer):
    """
    Serializer de Notificação para admin/funcionário (inclui dados de debug).
    """
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )
    canal_display = serializers.CharField(
        source='get_canal_display',
        read_only=True
    )
    
    class Meta:
        model = Notificacao
        fields = [
            'id', 'agendamento', 'tipo', 'tipo_display',
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'canal', 'canal_display', 'destinatario',
            'assunto', 'mensagem', 'enviada', 'data_envio',
            'tentativas', 'erro', 'data_criacao'
        ]
        read_only_fields = ['id', 'data_criacao']


class NotificacaoListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de notificações.
    """
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )
    
    class Meta:
        model = Notificacao
        fields = [
<<<<<<< HEAD
            'id', 'tipo_display',
=======
            'id', 'tipo_display', 'destinatario',
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'enviada', 'data_envio', 'data_criacao'
        ]
