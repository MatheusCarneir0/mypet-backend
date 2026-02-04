# apps/funcionarios/admin.py
from django.contrib import admin
<<<<<<< HEAD
from .models import Funcionario, HorarioTrabalho
=======
from .models import Funcionario
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cargo', 'horario_trabalho', 'ativo', 'data_criacao']
    list_filter = ['cargo', 'ativo', 'data_criacao']
    search_fields = ['usuario__nome', 'usuario__email']
    readonly_fields = ['data_criacao', 'data_atualizacao']

<<<<<<< HEAD

@admin.register(HorarioTrabalho)
class HorarioTrabalhoAdmin(admin.ModelAdmin):
    list_display = ['funcionario', 'dia_semana', 'hora_inicio', 'hora_fim', 'ativo']
    list_filter = ['dia_semana', 'ativo', 'funcionario']
    search_fields = ['funcionario__usuario__nome']


=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
