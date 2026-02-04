# apps/funcionarios/serializers.py
"""
Serializers para o app de funcionários.
"""
from rest_framework import serializers
from django.db import transaction
<<<<<<< HEAD
from django.contrib.auth.models import Group
from .models import Funcionario, HorarioTrabalho
from apps.authentication.models import Usuario
from apps.authentication.constants import UserGroups
from apps.authentication.serializers import UsuarioSerializer


class HorarioTrabalhoSerializer(serializers.ModelSerializer):
    """
    Serializer para o Horário de Trabalho.
    """
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)

    class Meta:
        model = HorarioTrabalho
        fields = ['id', 'funcionario', 'dia_semana', 'dia_semana_display', 'hora_inicio', 'hora_fim', 'ativo']
        read_only_fields = ['id', 'ativo']



=======
from .models import Funcionario
from apps.authentication.models import Usuario
from apps.authentication.serializers import UsuarioSerializer


>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
class FuncionarioSerializer(serializers.ModelSerializer):
    """
    Serializer base de Funcionário.
    """
    usuario = UsuarioSerializer(read_only=True)
<<<<<<< HEAD
    cargo_display = serializers.CharField(source='get_cargo_display', read_only=True)
    total_atendimentos = serializers.IntegerField(read_only=True)
    horarios = HorarioTrabalhoSerializer(source='horarios_trabalho', many=True, read_only=True)
=======
    cargo_display = serializers.CharField(
        source='get_cargo_display',
        read_only=True
    )
    total_atendimentos = serializers.IntegerField(read_only=True)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    class Meta:
        model = Funcionario
        fields = [
            'id', 'usuario', 'cargo', 'cargo_display',
<<<<<<< HEAD
            'horario_trabalho', 'horarios', 'total_atendimentos',
=======
            'horario_trabalho', 'total_atendimentos',
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'ativo', 'data_criacao', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'ativo', 'data_criacao', 'data_atualizacao']


class FuncionarioListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de funcionários.
    """
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    email = serializers.EmailField(source='usuario.email', read_only=True)
<<<<<<< HEAD
    cargo_display = serializers.CharField(source='get_cargo_display', read_only=True)
=======
    cargo_display = serializers.CharField(
        source='get_cargo_display',
        read_only=True
    )
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    class Meta:
        model = Funcionario
        fields = [
<<<<<<< HEAD
            'id', 'nome', 'email', 'cargo', 'cargo_display', 'horario_trabalho'
=======
            'id', 'nome', 'email', 'cargo_display', 'horario_trabalho'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        ]


class FuncionarioCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de funcionário.
    """
    # Campos do usuário
    email = serializers.EmailField(write_only=True)
    nome = serializers.CharField(write_only=True)
<<<<<<< HEAD
    telefone = serializers.CharField(write_only=True, required=False, allow_blank=True)
=======
    telefone = serializers.CharField(write_only=True)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    senha = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirmar_senha = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    # Campos do funcionário
    cargo = serializers.ChoiceField(choices=Funcionario.Cargo.choices)
<<<<<<< HEAD
=======
    horario_trabalho = serializers.CharField()
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    class Meta:
        model = Funcionario
        fields = [
            'email', 'nome', 'telefone', 'senha', 'confirmar_senha',
<<<<<<< HEAD
            'cargo'
=======
            'cargo', 'horario_trabalho'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        ]
    
    def validate(self, attrs):
        if attrs['senha'] != attrs.pop('confirmar_senha'):
            raise serializers.ValidationError({
                'confirmar_senha': 'As senhas não coincidem.'
            })
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        # Criar usuário
        usuario_data = {
            'email': validated_data.pop('email'),
            'nome': validated_data.pop('nome'),
<<<<<<< HEAD
            'telefone': validated_data.pop('telefone', ''),
            'senha': validated_data.pop('senha'),
        }
        usuario = Usuario.objects.create_user(**usuario_data)
        
        # Adicionar ao grupo FUNCIONARIO
        grupo_funcionario, _ = Group.objects.get_or_create(name=UserGroups.FUNCIONARIO)
        usuario.groups.add(grupo_funcionario)
        
        # Criar funcionário com um dummy para horario_trabalho exigido pelo model
        funcionario = Funcionario.objects.create(
            usuario=usuario,
            horario_trabalho='A definir',
=======
            'telefone': validated_data.pop('telefone'),
            'senha': validated_data.pop('senha'),
            'tipo_usuario': Usuario.TipoUsuario.FUNCIONARIO
        }
        usuario = Usuario.objects.create_user(**usuario_data)
        
        # Criar funcionário
        funcionario = Funcionario.objects.create(
            usuario=usuario,
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            **validated_data
        )
        
        return funcionario


class FuncionarioUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de funcionário.
    """
    nome = serializers.CharField(source='usuario.nome', required=False)
<<<<<<< HEAD
    telefone = serializers.CharField(source='usuario.telefone', required=False, allow_blank=True)
    email = serializers.EmailField(source='usuario.email', required=False)
=======
    telefone = serializers.CharField(source='usuario.telefone', required=False)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    class Meta:
        model = Funcionario
        fields = [
<<<<<<< HEAD
            'nome', 'telefone', 'email', 'cargo'
=======
            'nome', 'telefone', 'cargo', 'horario_trabalho'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        ]
    
    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', {})
        if usuario_data:
            for attr, value in usuario_data.items():
                setattr(instance.usuario, attr, value)
            instance.usuario.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
