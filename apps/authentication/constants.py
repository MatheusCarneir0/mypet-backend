# apps/authentication/constants.py

class UserGroups:
    """
    Constantes para os nomes dos grupos de usuários.
    Evita o uso de 'magic strings' pelo código.
    """
    CLIENTE = 'CLIENTE'
    FUNCIONARIO = 'FUNCIONARIO'
    ADMINISTRADOR = 'ADMINISTRADOR'
    SUPER_USUARIO = 'SUPER_USUARIO'
    
    @classmethod
    def choices(cls):
        return [
            (cls.CLIENTE, 'Cliente'),
            (cls.FUNCIONARIO, 'Funcionário'),
            (cls.ADMINISTRADOR, 'Administrador'),
            (cls.SUPER_USUARIO, 'Super Usuário'),
        ]
