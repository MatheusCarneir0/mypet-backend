# apps/authentication/models.py
"""
Modelo de usuário customizado.
Base para Cliente, Funcionario e Administrador.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
<<<<<<< HEAD
from .constants import UserGroups
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


class UsuarioManager(BaseUserManager):
    """
    Manager customizado para o modelo Usuario.
    """
    def create_user(self, email, senha=None, **extra_fields):
        """
        Cria e salva um usuário regular.
        """
        if not email:
            raise ValueError(_('O email é obrigatório'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, senha=None, **extra_fields):
        """
        Cria e salva um superusuário.
<<<<<<< HEAD
        Adiciona automaticamente ao grupo ADMINISTRADOR.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
=======
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo_usuario', Usuario.TipoUsuario.ADMINISTRADOR)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser deve ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser deve ter is_superuser=True.'))
        
<<<<<<< HEAD
        user = self.create_user(email, senha, **extra_fields)
        
        # Adicionar ao grupo ADMINISTRADOR
        from django.contrib.auth.models import Group
        admin_group, _ = Group.objects.get_or_create(name='ADMINISTRADOR')
        user.groups.add(admin_group)
        
        return user
=======
        return self.create_user(email, senha, **extra_fields)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


class Usuario(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Modelo de usuário customizado.
    Usa email como identificador único ao invés de username.
<<<<<<< HEAD
    Perfis de usuário são gerenciados via Django Groups (CLIENTE, FUNCIONARIO, ADMINISTRADOR).
    """
=======
    """
    class TipoUsuario(models.TextChoices):
        CLIENTE = 'CLIENTE', _('Cliente')
        FUNCIONARIO = 'FUNCIONARIO', _('Funcionário')
        ADMINISTRADOR = 'ADMINISTRADOR', _('Administrador')
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={
            'unique': _('Já existe um usuário com este email.'),
        }
    )
    nome = models.CharField(_('Nome Completo'), max_length=150)
    telefone = models.CharField(
        _('Telefone'),
<<<<<<< HEAD
        max_length=20,
        blank=True,
        default='',
=======
        max_length=15,
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        help_text='Formato: (88) 99999-9999'
    )
    foto = models.ImageField(
        _('Foto de Perfil'),
        upload_to='usuarios/fotos/',
        blank=True,
        null=True,
        help_text='Foto de perfil do usuário'
    )
<<<<<<< HEAD
    is_active = models.BooleanField(_('Ativo'), default=True)
    
    @property
    def ativo(self):
        return self.is_active
    
    @ativo.setter
    def ativo(self, value):
        self.is_active = value
    
=======
    tipo_usuario = models.CharField(
        _('Tipo de Usuário'),
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.CLIENTE
    )
    ativo = models.BooleanField(_('Ativo'), default=True)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    is_staff = models.BooleanField(_('Staff'), default=False)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'telefone']
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['email']),
<<<<<<< HEAD
            models.Index(fields=['is_active']),
=======
            models.Index(fields=['tipo_usuario', 'ativo']),
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        ]
    
    def __str__(self):
        return f'{self.nome} ({self.email})'
    
    def get_full_name(self):
        return self.nome
    
    def get_short_name(self):
        return self.nome.split()[0] if self.nome else ''
    
    @property
    def is_cliente(self):
<<<<<<< HEAD
        """Verifica se o usuário pertence ao grupo CLIENTE."""
        return self.groups.filter(name=UserGroups.CLIENTE).exists()
    
    @property
    def is_funcionario(self):
        """Verifica se o usuário pertence ao grupo FUNCIONARIO."""
        return self.groups.filter(name=UserGroups.FUNCIONARIO).exists()
    
    @property
    def is_administrador(self):
        """Verifica se o usuário pertence a grupo administrativo."""
        return self.groups.filter(
            name__in=[UserGroups.ADMINISTRADOR, UserGroups.SUPER_USUARIO]
        ).exists()
    
    def get_grupos(self):
        """Retorna lista com nomes dos grupos do usuário."""
        return list(self.groups.values_list('name', flat=True))
=======
        return self.tipo_usuario == self.TipoUsuario.CLIENTE
    
    @property
    def is_funcionario(self):
        return self.tipo_usuario == self.TipoUsuario.FUNCIONARIO
    
    @property
    def is_administrador(self):
        return self.tipo_usuario == self.TipoUsuario.ADMINISTRADOR
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)

