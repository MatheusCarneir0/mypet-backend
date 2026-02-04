# apps/servicos/serializers.py
"""
Serializers para o app de serviços.
"""
from rest_framework import serializers
from .models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    """
    Serializer de Serviço.
    """
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )
    
    class Meta:
        model = Servico
        fields = [
            'id', 'tipo', 'tipo_display', 'descricao',
<<<<<<< HEAD
            'preco', 'duracao_minutos', 'duracao_medio_grande', 'ativo',
=======
            'preco', 'duracao_minutos', 'ativo',
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'data_criacao', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao']


class ServicoListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de serviços.
    """
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )
    
    class Meta:
        model = Servico
        fields = [
<<<<<<< HEAD
            'id', 'tipo', 'tipo_display', 'descricao', 'preco', 'duracao_minutos', 'duracao_medio_grande'
=======
            'id', 'tipo', 'tipo_display', 'preco', 'duracao_minutos'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        ]


class ServicoCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e atualização de serviço.
    """
    class Meta:
        model = Servico
        fields = [
<<<<<<< HEAD
            'id', 'tipo', 'descricao', 'preco', 'duracao_minutos', 'duracao_medio_grande'
        ]
        read_only_fields = ['id']
=======
            'tipo', 'descricao', 'preco', 'duracao_minutos'
        ]
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    def validate_preco(self, value):
        if value < 0:
            raise serializers.ValidationError('O preço não pode ser negativo.')
        return value
    
    def validate_duracao_minutos(self, value):
        if value <= 0:
            raise serializers.ValidationError('A duração deve ser maior que zero.')
        if value > 480:  # 8 horas
            raise serializers.ValidationError('Duração muito longa.')
        return value
