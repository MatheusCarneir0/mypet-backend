# scripts/seed_data.py
"""
Script para popular banco de dados com dados de teste.
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import Usuario
from apps.clientes.models import Cliente
from apps.servicos.models import Servico
from apps.funcionarios.models import Funcionario
from apps.pagamentos.models import FormaPagamento


def criar_admin():
    """Cria usuário administrador."""
<<<<<<< HEAD
    from django.contrib.auth.models import Group
    
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    admin, created = Usuario.objects.get_or_create(
        email='admin@farmavet.com',
        defaults={
            'nome': 'Administrador FarmaVet',
            'telefone': '88999999999',
<<<<<<< HEAD
=======
            'tipo_usuario': Usuario.TipoUsuario.ADMINISTRADOR,
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
<<<<<<< HEAD
        
        admin_group, _ = Group.objects.get_or_create(name='ADMINISTRADOR')
        admin.groups.add(admin_group)
        
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        print('✓ Admin criado: admin@farmavet.com / admin123')


def criar_servicos():
<<<<<<< HEAD
    """Cria serviços padrão da FarmaVet."""
    servicos = [
        {
            'tipo': Servico.TipoServico.BANHO,
            'descricao': 'Banho completo com shampoo especial. Porte pequeno ~30min, médio/grande ~50min.',
            'preco': 50.00,
            'duracao_minutos': 30,
            'duracao_medio_grande': 50
=======
    """Cria serviços padrão."""
    servicos = [
        {
            'tipo': Servico.TipoServico.BANHO,
            'descricao': 'Banho completo com shampoo especial',
            'preco': 50.00,
            'duracao_minutos': 60
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        },
        {
            'tipo': Servico.TipoServico.TOSA,
            'descricao': 'Tosa higiênica ou estética',
            'preco': 70.00,
<<<<<<< HEAD
            'duracao_minutos': 80,
            'duracao_medio_grande': 80
        },
        {
            'tipo': Servico.TipoServico.BANHO_TOSA,
            'descricao': 'Banho completo + tosa (requer tosador e atendente)',
            'preco': 100.00,
            'duracao_minutos': 120,
            'duracao_medio_grande': 120
        },
        {
            'tipo': Servico.TipoServico.CORTE_UNHAS,
            'descricao': 'Corte de unhas para pets de pequeno, médio e grande porte',
            'preco': 25.00,
            'duracao_minutos': 15,
            'duracao_medio_grande': 20
        },
        {
            'tipo': Servico.TipoServico.BANHO_TERAPEUTICO,
            'descricao': 'Banho terapêutico com produtos medicamentosos para tratamento de pele',
            'preco': 80.00,
            'duracao_minutos': 40,
            'duracao_medio_grande': 60
        },
        {
            'tipo': Servico.TipoServico.VETERINARIO,
            'descricao': 'Atendimento com médico veterinário (tempo variável conforme situação)',
            'preco': 150.00,
            'duracao_minutos': 30,
            'duracao_medio_grande': 30
=======
            'duracao_minutos': 90
        },
        {
            'tipo': Servico.TipoServico.BANHO_TOSA,
            'descricao': 'Banho completo + tosa',
            'preco': 100.00,
            'duracao_minutos': 120
        },
        {
            'tipo': Servico.TipoServico.VETERINARIO,
            'descricao': 'Consulta veterinária',
            'preco': 150.00,
            'duracao_minutos': 30
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        },
    ]
    
    for servico_data in servicos:
<<<<<<< HEAD
        Servico.objects.update_or_create(
=======
        Servico.objects.get_or_create(
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            tipo=servico_data['tipo'],
            defaults=servico_data
        )
    
<<<<<<< HEAD
    print(f'✓ {len(servicos)} serviços criados/atualizados')


def criar_formas_pagamento():
    """Cria formas de pagamento padrão: Dinheiro, PIX e Cartão."""
=======
    print(f'✓ {len(servicos)} serviços criados')


def criar_formas_pagamento():
    """Cria formas de pagamento padrão."""
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    formas = [
        {
            'nome': 'Dinheiro',
            'tipo': FormaPagamento.TipoPagamento.DINHEIRO,
            'descricao': 'Pagamento em dinheiro'
        },
        {
<<<<<<< HEAD
=======
            'nome': 'Cartão de Débito',
            'tipo': FormaPagamento.TipoPagamento.CARTAO_DEBITO,
            'descricao': 'Pagamento com cartão de débito'
        },
        {
            'nome': 'Cartão de Crédito',
            'tipo': FormaPagamento.TipoPagamento.CARTAO_CREDITO,
            'descricao': 'Pagamento com cartão de crédito'
        },
        {
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            'nome': 'PIX',
            'tipo': FormaPagamento.TipoPagamento.PIX,
            'descricao': 'Pagamento via PIX'
        },
        {
<<<<<<< HEAD
            'nome': 'Cartão',
            'tipo': FormaPagamento.TipoPagamento.CARTAO_CREDITO,
            'descricao': 'Pagamento com cartão (débito ou crédito)'
=======
            'nome': 'Pagar na Loja',
            'tipo': FormaPagamento.TipoPagamento.DINHEIRO,
            'descricao': 'Pagamento a ser realizado no estabelecimento'
        },
        {
            'nome': 'Pagar na Entrega',
            'tipo': FormaPagamento.TipoPagamento.DINHEIRO,
            'descricao': 'Pagamento a ser realizado no momento da entrega'
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        },
    ]
    
    for forma_data in formas:
<<<<<<< HEAD
        FormaPagamento.objects.update_or_create(
=======
        FormaPagamento.objects.get_or_create(
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            nome=forma_data['nome'],
            defaults=forma_data
        )
    
<<<<<<< HEAD
    print(f'✓ {len(formas)} formas de pagamento criadas/atualizadas')
=======
    print(f'✓ {len(formas)} formas de pagamento criadas')
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


def criar_cliente_teste():
    """Cria cliente de teste."""
<<<<<<< HEAD
    from django.contrib.auth.models import Group
    
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    usuario, created = Usuario.objects.get_or_create(
        email='cliente@test.com',
        defaults={
            'nome': 'Cliente Teste',
<<<<<<< HEAD
            'telefone': '88988888888'
=======
            'telefone': '88988888888',
            'tipo_usuario': Usuario.TipoUsuario.CLIENTE
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        }
    )
    if created:
        usuario.set_password('cliente123')
        usuario.save()
        
<<<<<<< HEAD
        cliente_group, _ = Group.objects.get_or_create(name='CLIENTE')
        usuario.groups.add(cliente_group)
        
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        Cliente.objects.create(
            usuario=usuario,
            cpf='123.456.789-00',
            endereco='Rua Teste, 123',
<<<<<<< HEAD
            ponto_referencia='Próximo ao mercado central',
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            cidade='Boa Viagem',
            estado='CE',
            cep='63870-000'
        )
        
        print('✓ Cliente teste criado: cliente@test.com / cliente123')


<<<<<<< HEAD
def criar_funcionario_teste():
    """Cria funcionário de teste (tosador)."""
    from django.contrib.auth.models import Group

    usuario, created = Usuario.objects.get_or_create(
        email='funcionario@test.com',
        defaults={
            'nome': 'Funcionário Teste',
            'telefone': '88977777777'
        }
    )
    if created:
        usuario.set_password('func123')
        usuario.save()

        func_group, _ = Group.objects.get_or_create(name='FUNCIONARIO')
        usuario.groups.add(func_group)

        Funcionario.objects.create(
            usuario=usuario,
            cargo=Funcionario.Cargo.TOSADOR,
            horario_trabalho='Segunda a Sábado, 07:00-17:30'
        )

        print('✓ Funcionário teste criado: funcionario@test.com / func123')
    else:
        print('  Funcionário teste já existe')


def regenerar_horarios_trabalho():
    """Re-salva todos os funcionários para regenerar HorarioTrabalho com intervalo de almoço."""
    count = 0
    for func in Funcionario.objects.all():
        func.save()
        count += 1
    print(f'✓ Horários de trabalho regenerados para {count} funcionário(s)')


=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
def main():
    """Executa todos os seeds."""
    print('🌱 Populando banco de dados...\n')
    
    criar_admin()
    criar_servicos()
    criar_formas_pagamento()
    criar_cliente_teste()
<<<<<<< HEAD
    criar_funcionario_teste()
    regenerar_horarios_trabalho()
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    print('\n✅ Banco de dados populado com sucesso!')


if __name__ == '__main__':
    main()

