# apps/clientes/serializers.py
"""
Serializers para o app de clientes.
"""
from rest_framework import serializers
from django.db import transaction
<<<<<<< HEAD
from drf_spectacular.utils import extend_schema_field
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
from .models import Cliente
from apps.authentication.models import Usuario
from apps.authentication.serializers import UsuarioSerializer


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer base de Cliente.
    """
    usuario = UsuarioSerializer(read_only=True)
    total_pets = serializers.IntegerField(read_only=True)
    total_agendamentos = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = [
<<<<<<< HEAD
            'id', 'usuario', 'cpf', 'endereco', 'ponto_referencia', 'cidade',
=======
            'id', 'usuario', 'cpf', 'endereco', 'cidade',
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'estado', 'cep', 'total_pets', 'total_agendamentos',
            'ativo', 'data_criacao', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'ativo', 'data_criacao', 'data_atualizacao']


class ClienteListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de clientes.
    """
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    email = serializers.EmailField(source='usuario.email', read_only=True)
    telefone = serializers.CharField(source='usuario.telefone', read_only=True)
    total_pets = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'email', 'telefone', 'cpf',
            'cidade', 'estado', 'total_pets'
        ]


class ClienteCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de cliente.
    Cria o usuário e o cliente em uma transação.
    """
    # Campos do usuário
    email = serializers.EmailField(write_only=True)
    nome = serializers.CharField(write_only=True)
    telefone = serializers.CharField(write_only=True)
    senha = serializers.CharField(write_only=True, style={'input_type': 'password'})
<<<<<<< HEAD
    confirmar_senha = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    
    # Campos do cliente
    cpf = serializers.CharField(required=False, allow_blank=True, default='')
    endereco = serializers.CharField(required=False, allow_blank=True, default='')
    ponto_referencia = serializers.CharField(required=False, allow_blank=True, default='')
    cidade = serializers.CharField(required=False, allow_blank=True, default='')
    estado = serializers.CharField(required=False, allow_blank=True, default='')
    cep = serializers.CharField(required=False, allow_blank=True, default='')
=======
    confirmar_senha = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    # Campos do cliente
    cpf = serializers.CharField()
    endereco = serializers.CharField()
    cidade = serializers.CharField()
    estado = serializers.CharField()
    cep = serializers.CharField()
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    class Meta:
        model = Cliente
        fields = [
            'email', 'nome', 'telefone', 'senha', 'confirmar_senha',
<<<<<<< HEAD
            'cpf', 'endereco', 'ponto_referencia', 'cidade', 'estado', 'cep'
=======
            'cpf', 'endereco', 'cidade', 'estado', 'cep'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        ]
    
    def validate(self, attrs):
        """
        Validação customizada.
        """
        # Validar senhas
<<<<<<< HEAD
        confirmar_senha = attrs.pop('confirmar_senha', None)
        if confirmar_senha is not None and attrs['senha'] != confirmar_senha:
=======
        if attrs['senha'] != attrs.pop('confirmar_senha'):
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            raise serializers.ValidationError({
                'confirmar_senha': 'As senhas não coincidem.'
            })
        
<<<<<<< HEAD
        # Validar CPF único (apenas se informado)
        cpf = attrs.get('cpf', '')
        if cpf and Cliente.objects.filter(cpf=cpf, ativo=True).exists():
=======
        # Validar CPF único
        cpf = attrs.get('cpf')
        if Cliente.objects.filter(cpf=cpf, ativo=True).exists():
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            raise serializers.ValidationError({
                'cpf': 'Já existe um cliente cadastrado com este CPF.'
            })
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Criar usuário e cliente em uma transação atômica.
        """
        from .services import ClienteService
        
        # Extrair dados do usuário
        usuario_data = {
            'email': validated_data.pop('email'),
            'nome': validated_data.pop('nome'),
            'telefone': validated_data.pop('telefone'),
            'senha': validated_data.pop('senha'),
        }
        
        # Criar cliente via service
        cliente = ClienteService.criar_cliente(usuario_data, validated_data)
        
        return cliente


class ClienteUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de cliente.
    """
    # Permitir atualizar dados do usuário também
    nome = serializers.CharField(source='usuario.nome', required=False)
    telefone = serializers.CharField(source='usuario.telefone', required=False)
    
    class Meta:
        model = Cliente
        fields = [
<<<<<<< HEAD
            'nome', 'telefone', 'endereco', 'ponto_referencia',
=======
            'nome', 'telefone', 'endereco',
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'cidade', 'estado', 'cep'
        ]
    
    def update(self, instance, validated_data):
        """
        Atualizar cliente e usuário.
        """
        # Atualizar dados do usuário se fornecidos
        usuario_data = validated_data.pop('usuario', {})
        if usuario_data:
            for attr, value in usuario_data.items():
                setattr(instance.usuario, attr, value)
            instance.usuario.save()
        
        # Atualizar dados do cliente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class ClienteDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detalhado de cliente com relacionamentos.
    """
    usuario = UsuarioSerializer(read_only=True)
    pets = serializers.SerializerMethodField()
    total_agendamentos = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = [
<<<<<<< HEAD
            'id', 'usuario', 'cpf', 'endereco', 'ponto_referencia', 'cidade',
=======
            'id', 'usuario', 'cpf', 'endereco', 'cidade',
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'estado', 'cep', 'pets', 'total_agendamentos',
            'ativo', 'data_criacao', 'data_atualizacao'
        ]
    
<<<<<<< HEAD
    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    def get_pets(self, obj):
        """
        Retornar lista resumida de pets.
        """
        from apps.pets.serializers import PetListSerializer
        pets = obj.pets.filter(ativo=True)
        return PetListSerializer(pets, many=True).data
