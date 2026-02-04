# apps/clientes/services.py
"""
Services para operações de clientes.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
<<<<<<< HEAD
from django.contrib.auth.models import Group
from .models import Cliente
from apps.authentication.models import Usuario
from apps.authentication.constants import UserGroups
=======
from .models import Cliente
from apps.authentication.models import Usuario
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


class ClienteService:
    """
    Service para operações de cliente.
    """
    
    @staticmethod
    @transaction.atomic
    def criar_cliente(dados_usuario, dados_cliente):
        """
        Cria um cliente completo (usuário + cliente).
<<<<<<< HEAD
        Adiciona automaticamente ao grupo CLIENTE.
        
        Args:
            dados_usuario: dict com dados do usuário (email, nome, telefone, senha)
            dados_cliente: dict com dados do cliente (cpf, endereco, cidade, estado, cep)
=======
        
        Args:
            dados_usuario: dict com dados do usuário
            dados_cliente: dict com dados do cliente
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        
        Returns:
            Cliente: Instância do cliente criado
        """
<<<<<<< HEAD
        email = dados_usuario.get('email')
        cpf = dados_cliente.get('cpf')

        # Verificar se email já existe
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Já existe um usuário com este email.')
        
        # Verificar se CPF já existe
        if Cliente.objects.filter(cpf=cpf, ativo=True).exists():
=======
        # Verificar se email já existe
        if Usuario.objects.filter(email=dados_usuario['email']).exists():
            raise ValidationError('Já existe um usuário com este email.')
        
        # Verificar se CPF já existe
        if Cliente.objects.filter(cpf=dados_cliente['cpf'], ativo=True).exists():
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            raise ValidationError('Já existe um cliente com este CPF.')
        
        # Criar usuário
        usuario = Usuario.objects.create_user(
<<<<<<< HEAD
            email=email,
            nome=dados_usuario['nome'],
            telefone=dados_usuario['telefone'],
            senha=dados_usuario['senha']
        )
        
        # Adicionar ao grupo CLIENTE
        grupo_cliente, _ = Group.objects.get_or_create(name=UserGroups.CLIENTE)
        usuario.groups.add(grupo_cliente)
        
=======
            email=dados_usuario['email'],
            nome=dados_usuario['nome'],
            telefone=dados_usuario['telefone'],
            senha=dados_usuario['senha'],
            tipo_usuario=Usuario.TipoUsuario.CLIENTE
        )
        
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        # Criar cliente
        cliente = Cliente.objects.create(
            usuario=usuario,
            **dados_cliente
        )
        
        return cliente
    
    @staticmethod
    def obter_cliente_por_usuario(usuario):
        """
        Obtém o cliente associado a um usuário.
        """
<<<<<<< HEAD
        if not hasattr(usuario, 'cliente'):
             raise ValidationError('Cliente não encontrado para este usuário.')
        return usuario.cliente
=======
        try:
            return usuario.cliente
        except Cliente.DoesNotExist:
            raise ValidationError('Cliente não encontrado para este usuário.')
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    @staticmethod
    def atualizar_cliente(cliente, dados):
        """
<<<<<<< HEAD
        Atualiza dados do cliente de forma segura.
        Ignora campos que não devem ser atualizados via service genérico.
        """
        # Lista de campos permitidos para atualização
        campos_permitidos = {'endereco', 'cidade', 'estado', 'cep', 'telefone'}
        
        # Atualiza campos do Cliente
        alterado = False
        for campo, valor in dados.items():
            if campo in campos_permitidos and hasattr(cliente, campo):
                setattr(cliente, campo, valor)
                alterado = True
                
        # Atualiza campos do Usuário se necessário (ex: telefone)
        if 'telefone' in dados:
             cliente.usuario.telefone = dados['telefone']
             cliente.usuario.save()

        if alterado:
            cliente.save()
            
=======
        Atualiza dados do cliente.
        """
        for campo, valor in dados.items():
            setattr(cliente, campo, valor)
        
        cliente.save()
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        return cliente

