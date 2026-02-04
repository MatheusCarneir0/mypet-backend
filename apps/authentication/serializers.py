# apps/authentication/serializers.py
"""
Serializers para autenticação e gerenciamento de usuários.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from .models import Usuario
<<<<<<< HEAD
from drf_spectacular.utils import extend_schema_field
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer base de Usuario.
<<<<<<< HEAD
    Inclui grupos do usuário para controle de permissões.
    """
    groups = serializers.SerializerMethodField()
    cliente_id = serializers.SerializerMethodField()
    # #9: SerializerMethodField com type hint para resolver warning do Swagger
    ativo = serializers.SerializerMethodField()

=======
    """
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'nome', 'telefone', 'foto',
<<<<<<< HEAD
            'groups', 'cliente_id', 'ativo', 'data_criacao'
        ]
        read_only_fields = ['id', 'groups', 'cliente_id', 'data_criacao']

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_groups(self, obj):
        """Retorna lista de nomes dos grupos do usuário."""
        return obj.get_grupos()

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_cliente_id(self, obj):
        """Retorna o ID do perfil de cliente, se existir."""
        try:
            return obj.cliente.id
        except Exception:
            return None

    @extend_schema_field(serializers.BooleanField())
    def get_ativo(self, obj):
        """Retorna se o usuário está ativo (usa campo is_active do DB)."""
        return obj.is_active

=======
            'tipo_usuario', 'ativo', 'data_criacao'
        ]
        read_only_fields = ['id', 'tipo_usuario', 'data_criacao']
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de usuário.
    """
    senha = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    confirmar_senha = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Usuario
        fields = [
            'email', 'nome', 'telefone', 
<<<<<<< HEAD
            'senha', 'confirmar_senha'
=======
            'senha', 'confirmar_senha', 'tipo_usuario'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        ]
    
    def validate(self, attrs):
        """
        Validação customizada.
        """
        # Validar senhas
        if attrs['senha'] != attrs.pop('confirmar_senha'):
            raise serializers.ValidationError({
                'confirmar_senha': 'As senhas não coincidem.'
            })
        
        # Validar força da senha
        try:
            validate_password(attrs['senha'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({
                'senha': list(e.messages)
            })
        
        return attrs
    
    def create(self, validated_data):
        """
        Criar usuário com senha hash.
        """
        senha = validated_data.pop('senha')
        usuario = Usuario.objects.create_user(
            senha=senha,
            **validated_data
        )
        return usuario


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado para JWT token.
    Adiciona informações extras ao token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Adicionar claims customizados
        token['nome'] = user.nome
        token['email'] = user.email
<<<<<<< HEAD
        token['groups'] = user.get_grupos()  # Lista de grupos ao invés de tipo_usuario
=======
        token['tipo_usuario'] = user.tipo_usuario
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Adicionar dados extras à resposta
<<<<<<< HEAD
        # data['usuario'] = {
        #     'id': self.user.id,
        #     'email': self.user.email,
        #     'nome': self.user.nome,
        #     'groups': self.user.get_grupos(),  # Lista de grupos ao invés de tipo_usuario
        # }
=======
        data['usuario'] = {
            'id': self.user.id,
            'email': self.user.email,
            'nome': self.user.nome,
            'tipo_usuario': self.user.tipo_usuario,
        }
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        
        return data


class AlterarSenhaSerializer(serializers.Serializer):
    """
    Serializer para alteração de senha.
    """
    senha_atual = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    senha_nova = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    confirmar_senha_nova = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        if attrs['senha_nova'] != attrs['confirmar_senha_nova']:
            raise serializers.ValidationError({
                'confirmar_senha_nova': 'As senhas não coincidem.'
            })
        
        try:
            validate_password(attrs['senha_nova'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({
                'senha_nova': list(e.messages)
            })
        
        return attrs


<<<<<<< HEAD
=======
class GoogleLoginSerializer(serializers.Serializer):
    """
    Serializer para login com Google.
    """
    token = serializers.CharField(required=True, help_text='Token de acesso do Google')
    email = serializers.EmailField(required=True)
    nome = serializers.CharField(required=True)
    foto_url = serializers.URLField(required=False, allow_blank=True)


>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
class UploadFotoSerializer(serializers.Serializer):
    """
    Serializer para upload de foto de perfil.
    """
    foto = serializers.ImageField(required=True)
<<<<<<< HEAD


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer para solicitar redefinição de senha via email.
    """
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer para confirmar nova senha usando uid + token.
    """
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    senha_nova = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
    )
    confirmar_senha = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        if attrs['senha_nova'] != attrs['confirmar_senha']:
            raise serializers.ValidationError({
                'confirmar_senha': 'As senhas não coincidem.'
            })
        try:
            validate_password(attrs['senha_nova'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({'senha_nova': list(e.messages)})
        return attrs
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
