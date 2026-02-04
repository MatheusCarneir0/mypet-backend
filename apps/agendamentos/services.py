# apps/agendamentos/services.py
"""
Services para operações de agendamentos.
Este é um dos services mais complexos do sistema.
<<<<<<< HEAD
Atualizado para utilizar Service Layers Pattern, eliminando N+1 Queries.
"""
import logging
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, datetime
from typing import Optional, List, Dict

from .models import Agendamento
from apps.pets.models import Pet
from apps.servicos.models import Servico
from apps.funcionarios.models import Funcionario, HorarioTrabalho
from apps.agendamentos.repositories import AgendamentoRepository
from apps.agendamentos.validators import AgendamentoValidator
from apps.core.audit import AuditLogger

logger = logging.getLogger(__name__)
=======
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Agendamento
from apps.pets.models import Pet
from apps.servicos.models import Servico
from apps.funcionarios.models import Funcionario
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)


class AgendamentoService:
    """
    Service para operações de agendamento.
    """
    
<<<<<<< HEAD
    # Portes considerados médio/grande para duração diferenciada
    PORTES_MEDIO_GRANDE = {'MEDIO', 'GRANDE', 'GIGANTE'}

    @staticmethod
    def _funcionario_livre_no_slot(funcionario, data_hora_slot, duracao, cache_agendamentos=None, agendamento_ignorado_id=None):
        """Valida disponibilidade de um funcionario no slot considerando expediente e conflitos."""
        dentro_expediente = AgendamentoValidator.validar_horario_dentro_expediente(
            data_hora_slot.time(), duracao, funcionario.expedientes_hoje
        )
        if not dentro_expediente:
            return False

        tem_conflito = AgendamentoRepository.verificar_conflito_horario(
            funcionario.id,
            data_hora_slot,
            duracao,
            cache_agendamentos=cache_agendamentos,
            agendamento_ignorado_id=agendamento_ignorado_id,
        )
        return not tem_conflito

    @staticmethod
    def _obter_equipe_banho_tosa_livre(funcionarios, data_hora_slot, duracao, cache_agendamentos=None, agendamento_ignorado_id=None):
        """
        Para BANHO_TOSA, exige equipe minima: 1 TOSADOR e 1 ATENDENTE livres no mesmo slot.
        Retorna tupla (tosador, atendente) ou (None, None) quando indisponivel.
        """
        tosador_livre = None
        atendente_livre = None

        for func in funcionarios:
            if func.cargo == Funcionario.Cargo.TOSADOR and tosador_livre is None:
                if AgendamentoService._funcionario_livre_no_slot(
                    func,
                    data_hora_slot,
                    duracao,
                    cache_agendamentos=cache_agendamentos,
                    agendamento_ignorado_id=agendamento_ignorado_id,
                ):
                    tosador_livre = func
            elif func.cargo == Funcionario.Cargo.ATENDENTE and atendente_livre is None:
                if AgendamentoService._funcionario_livre_no_slot(
                    func,
                    data_hora_slot,
                    duracao,
                    cache_agendamentos=cache_agendamentos,
                    agendamento_ignorado_id=agendamento_ignorado_id,
                ):
                    atendente_livre = func

            if tosador_livre and atendente_livre:
                return tosador_livre, atendente_livre

        return None, None
    
    @staticmethod
    def obter_duracao_servico(servico, pet=None):
        """
        Retorna a duração do serviço considerando o porte do pet.
        Se o pet for de porte médio/grande/gigante e o serviço tiver
        duracao_medio_grande definida, usa essa duração.
        """
        if (pet and 
            pet.porte in AgendamentoService.PORTES_MEDIO_GRANDE and 
            servico.duracao_medio_grande):
            return servico.duracao_medio_grande
        return servico.duracao_minutos
    
    @staticmethod
    def _get_dia_semana_bd(data) -> int:
        """
        Converte o weekday do Python (0=Segunda) para o nosso BD (0=Domingo).
        """
        return (data.weekday() + 1) % 7
        
    @staticmethod
    def horarios_disponiveis(data, servico_id, pet_id=None) -> List[Dict]:
        """
        Retorna horários disponíveis otimizados usando Repository.
        Se pet_id informado, calcula duração com base no porte do pet.
        """
        # 1. Obter serviço (1 Query)
=======
    @staticmethod
    def horarios_disponiveis(data, servico_id):
        """
        Retorna horários disponíveis para um serviço em uma data.
        
        Args:
            data: Data para consulta
            servico_id: ID do serviço
        
        Returns:
            list: Lista de horários disponíveis
        """
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        try:
            servico = Servico.objects.get(id=servico_id)
        except Servico.DoesNotExist:
            raise ValidationError('Serviço não encontrado.')
        
<<<<<<< HEAD
        # Determinar duração com base no porte do pet
        pet = None
        if pet_id:
            try:
                pet = Pet.objects.get(id=pet_id)
            except Pet.DoesNotExist:
                pass
        duracao = AgendamentoService.obter_duracao_servico(servico, pet)
        
        dia_semana = AgendamentoService._get_dia_semana_bd(data)
        
        # 2. Obter Equipe e Grade (1 Query via SubQuery/Prefetch)
        funcionarios_ativos = AgendamentoRepository.buscar_funcionarios_disponiveis_com_expedientes(
            servico, dia_semana
        )
        
        logger.info(f"Otimização DB - Funcionários escalados no Dia {dia_semana}: {len(funcionarios_ativos)}")
        if not funcionarios_ativos:
            return []
            
        # 3. Cachear agendamentos do dia (1 Query)
        agendamentos_cache = AgendamentoRepository.buscar_agendamentos_do_dia(data)
        
        # Obter a faixa máxima global para o dia
        min_hour = min(e.hora_inicio for f in funcionarios_ativos for e in f.expedientes_hoje)
        max_hour = max(e.hora_fim for f in funcionarios_ativos for e in f.expedientes_hoje)
        
        horarios = []
        hora_atual_time = datetime.combine(data, min_hour)
        hora_fim_time = datetime.combine(data, max_hour)
        
        # Loop In-Memory de O(1) TimeBox
        while hora_atual_time < hora_fim_time:
            data_hora_slot = timezone.make_aware(hora_atual_time)
            
            # Não retornar slots que já passaram
            if data_hora_slot <= timezone.now():
                hora_atual_time += timedelta(minutes=30)
                continue
            
            slot_livre = False
            
            # Se pet_id informado, verificar se o pet já tem agendamento neste horário
            if pet and AgendamentoRepository.verificar_conflito_pet(pet.id, data_hora_slot, duracao):
                slot_livre = False
            elif servico.tipo == Servico.TipoServico.BANHO_TOSA:
                # BANHO_TOSA exige equipe minima com 1 tosador + 1 atendente livres.
                tosador, atendente = AgendamentoService._obter_equipe_banho_tosa_livre(
                    funcionarios_ativos,
                    data_hora_slot,
                    duracao,
                    cache_agendamentos=agendamentos_cache,
                )
                slot_livre = bool(tosador and atendente)
            else:
                for func in funcionarios_ativos:
                    # Validar In-Memory Expediente
                    dentro_expediente = AgendamentoValidator.validar_horario_dentro_expediente(
                        data_hora_slot.time(), 
                        duracao, 
                        func.expedientes_hoje
                    )
                    
                    if dentro_expediente:
                        # Validar In-Memory Agenda
                        tem_conflito = AgendamentoRepository.verificar_conflito_horario(
                            func.id, 
                            data_hora_slot, 
                            duracao, 
                            cache_agendamentos=agendamentos_cache
                        )
                        if not tem_conflito:
                            slot_livre = True
                            break
            
            # Só retorna slots que estão livres
            if slot_livre:
                horarios.append({
                    'hora': data_hora_slot.strftime('%H:%M'),
                    'data_hora': data_hora_slot.isoformat(),
                    'disponivel': True
                })
            
            hora_atual_time += timedelta(minutes=30)
            
        return horarios

    @staticmethod
    def verificar_disponibilidade(data_hora, duracao_minutos):
        # Deprecated logic now mapped deeply to Repository patterns
        return True
        
    @staticmethod
    def _alocar_funcionario(data_hora, servico, pet=None, agendamento_ignorado_id=None):
        """
        Aloca um funcionário em runtime (ex: via POST Create).
        Para BANHO_TOSA, exige equipe minima (tosador + atendente) no mesmo slot.
        Para demais serviços, encontra qualquer funcionário livre.
        """
        # Converter para hora local para comparar com expedientes (armazenados em horário local)
        data_hora_local = timezone.localtime(data_hora)
        duracao = AgendamentoService.obter_duracao_servico(servico, pet)
        dia_semana_bd = AgendamentoService._get_dia_semana_bd(data_hora_local.date())
        funcionarios_aptos = AgendamentoRepository.buscar_funcionarios_disponiveis_com_expedientes(
            servico, dia_semana_bd
        )
        
        if servico.tipo == Servico.TipoServico.BANHO_TOSA:
            tosador, atendente = AgendamentoService._obter_equipe_banho_tosa_livre(
                funcionarios_aptos,
                data_hora,
                duracao,
                agendamento_ignorado_id=agendamento_ignorado_id,
            )
            if tosador and atendente:
                # Como o modelo atual persiste 1 responsavel, prioriza o tosador para rastreabilidade.
                return tosador
            return None
        
        for func in funcionarios_aptos:
            dentro_expediente = AgendamentoValidator.validar_horario_dentro_expediente(
                data_hora_local.time(), 
                duracao, 
                func.expedientes_hoje
            )
            
            if dentro_expediente:
                conflito = AgendamentoRepository.verificar_conflito_horario(
                    func.id, data_hora, duracao, agendamento_ignorado_id=agendamento_ignorado_id
                )
                if not conflito:
                    return func
        return None
=======
        horarios = []
        
        # Horário comercial: 8h às 18h
        hora_inicio = 8
        hora_fim = 18
        
        # Gerar slots de 30 em 30 minutos
        hora_atual = hora_inicio
        while hora_atual < hora_fim:
            data_hora = timezone.make_aware(
                datetime.combine(data, datetime.min.time().replace(hour=hora_atual))
            )
            
            # Verificar se horário está disponível
            if AgendamentoService.verificar_disponibilidade(data_hora, servico.duracao_minutos):
                horarios.append({
                    'hora': f'{hora_atual:02d}:00',
                    'data_hora': data_hora.isoformat(),
                    'disponivel': True
                })
            else:
                horarios.append({
                    'hora': f'{hora_atual:02d}:00',
                    'data_hora': data_hora.isoformat(),
                    'disponivel': False
                })
            
            hora_atual += 1
        
        return horarios
    
    @staticmethod
    def verificar_disponibilidade(data_hora, duracao_minutos):
        """
        Verifica se um horário está disponível.
        
        Args:
            data_hora: Data e hora para verificar
            duracao_minutos: Duração do serviço em minutos
        
        Returns:
            bool: True se disponível
        """
        # Calcular fim do agendamento
        fim = data_hora + timedelta(minutes=duracao_minutos)
        
        # Buscar agendamentos conflitantes
        conflitos = Agendamento.objects.filter(
            data_hora__lt=fim,
            data_hora__gte=data_hora,
            status__in=[
                Agendamento.Status.AGENDADO,
                Agendamento.Status.CONFIRMADO,
                Agendamento.Status.EM_ANDAMENTO
            ],
            ativo=True
        ).exists()
        
        return not conflitos
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
    
    @staticmethod
    @transaction.atomic
    def criar_agendamento(cliente, pet_id, servico_id, data_hora, forma_pagamento_id, observacoes=''):
        """
<<<<<<< HEAD
        Cria um novo agendamento validando negócio via Validators & Repository.
        """
        # 1. Busca instâncias base
=======
        Cria um novo agendamento.
        
        Args:
            cliente: Instância do cliente
            pet_id: ID do pet
            servico_id: ID do serviço
            data_hora: Data e hora do agendamento
            forma_pagamento_id: ID da forma de pagamento escolhida
            observacoes: Observações opcionais
        
        Returns:
            Agendamento: Instância do agendamento criado
        """
        # Validações
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            raise ValidationError('Pet não encontrado.')
<<<<<<< HEAD
            
        if not pet.ativo:
            raise ValidationError('Pet inativo.')
            
        valido_pet, err_pet = AgendamentoValidator.validar_pet_pertence_cliente(pet, cliente)
        if not valido_pet:
            raise ValidationError(err_pet)
=======
        
        if pet.cliente != cliente:
            raise ValidationError('O pet não pertence a este cliente.')
        
        if not pet.ativo:
            raise ValidationError('Pet inativo.')
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        
        try:
            servico = Servico.objects.get(id=servico_id)
        except Servico.DoesNotExist:
            raise ValidationError('Serviço não encontrado.')
<<<<<<< HEAD
            
        if not servico.ativo:
            raise ValidationError('Serviço inativo.')
            
=======
        
        if not servico.ativo:
            raise ValidationError('Serviço inativo.')
        
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        # Validar forma de pagamento
        try:
            from apps.pagamentos.models import FormaPagamento
            forma_pagamento = FormaPagamento.objects.get(id=forma_pagamento_id)
        except FormaPagamento.DoesNotExist:
            raise ValidationError('Forma de pagamento não encontrada.')
<<<<<<< HEAD
            
        if not forma_pagamento.ativo:
            raise ValidationError('Forma de pagamento inativa.')
            
        # 2. Validators Customizados (Tempo Futuro já deve vir garantido pela API Serializer, 
        #    mas service previne buracos na model layer).
        valido_futuro, err_fut = AgendamentoValidator.validar_data_hora_futura(data_hora)
        if not valido_futuro:
            raise ValidationError(err_fut)
            
        # 3. Verificar conflito de horário do pet (mesmo pet não pode estar em 2 serviços)
        duracao_real = AgendamentoService.obter_duracao_servico(servico, pet)
        if AgendamentoRepository.verificar_conflito_pet(pet.id, data_hora, duracao_real):
            raise ValidationError('Este pet já possui um agendamento neste horário.')
            
        # 4. Alocação
        funcionario = AgendamentoService._alocar_funcionario(data_hora, servico, pet=pet)
        if not funcionario:
            raise ValidationError('Horário indisponível (agendamentos em conflito ou fora de expediente).')
            
=======
        
        if not forma_pagamento.ativo:
            raise ValidationError('Forma de pagamento inativa.')
        
        # Verificar disponibilidade
        if not AgendamentoService.verificar_disponibilidade(
            data_hora, servico.duracao_minutos
        ):
            raise ValidationError('Horário indisponível.')
        
        # Alocar funcionário disponível (lógica simplificada)
        funcionario = AgendamentoService._alocar_funcionario(data_hora, servico)
        
        # Criar agendamento
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            pet=pet,
            servico=servico,
            funcionario=funcionario,
            forma_pagamento=forma_pagamento,
            data_hora=data_hora,
<<<<<<< HEAD
            duracao_real=duracao_real,
            observacoes=observacoes,
            status=Agendamento.Status.AGENDADO
        )

        # Auditoria — rastreabilidade LGPD
        AuditLogger.log_agendamento_criado(agendamento)
        
        # Enviar SMS/Notificação Assíncrona via Celery se disponível
=======
            observacoes=observacoes,
            status=Agendamento.Status.AGENDADO
        )
        
        # Enviar notificação de confirmação (se service existir)
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        try:
            from apps.notificacoes.services import NotificacaoService
            NotificacaoService.enviar_confirmacao_agendamento(agendamento)
        except ImportError:
<<<<<<< HEAD
            pass
            
        return agendamento
    
    @staticmethod
    @transaction.atomic
    def cancelar_agendamento(agendamento, motivo=''):
        """ Cancela de forma segura validando o status original. """
        if not agendamento.pode_cancelar:
            raise ValidationError('Este agendamento não pode ser cancelado (veja regras de Status).')
=======
            pass  # Service ainda não implementado
        
        return agendamento
    
    @staticmethod
    def _alocar_funcionario(data_hora, servico):
        """
        Aloca um funcionário disponível para o agendamento.
        Lógica simplificada - escolhe o primeiro disponível.
        """
        # Buscar funcionários ativos
        funcionarios = Funcionario.objects.filter(ativo=True)
        
        # Para veterinário, buscar apenas veterinários
        if servico.tipo == Servico.TipoServico.VETERINARIO:
            funcionarios = funcionarios.filter(cargo=Funcionario.Cargo.VETERINARIO)
        # Para banho/tosa, buscar tosadores
        elif servico.tipo in [Servico.TipoServico.BANHO, Servico.TipoServico.TOSA, Servico.TipoServico.BANHO_TOSA]:
            funcionarios = funcionarios.filter(cargo=Funcionario.Cargo.TOSADOR)
        
        # Verificar disponibilidade de cada um
        for funcionario in funcionarios:
            conflito = Agendamento.objects.filter(
                funcionario=funcionario,
                data_hora=data_hora,
                status__in=[
                    Agendamento.Status.AGENDADO,
                    Agendamento.Status.CONFIRMADO,
                    Agendamento.Status.EM_ANDAMENTO
                ],
                ativo=True
            ).exists()
            
            if not conflito:
                return funcionario
        
        return None  # Nenhum funcionário disponível
    
    @staticmethod
    @transaction.atomic
    def cancelar_agendamento(agendamento, motivo=''):
        """
        Cancela um agendamento.
        """
        if not agendamento.pode_cancelar:
            raise ValidationError('Este agendamento não pode ser cancelado.')
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        
        agendamento.status = Agendamento.Status.CANCELADO
        if motivo:
            agendamento.observacoes += f'\nMotivo do cancelamento: {motivo}'
        agendamento.save()
<<<<<<< HEAD

        # Auditoria — rastreabilidade de cancelamentos
        AuditLogger.log_agendamento_cancelado(agendamento, motivo)
        
=======
        
        # Enviar notificação de cancelamento
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        try:
            from apps.notificacoes.services import NotificacaoService
            NotificacaoService.enviar_cancelamento_agendamento(agendamento)
        except ImportError:
            pass
<<<<<<< HEAD
            
=======
        
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        return agendamento
    
    @staticmethod
    @transaction.atomic
<<<<<<< HEAD
    def reagendar(agendamento, nova_data_hora, forma_pagamento_id=None, force=False):
        """ Reagenda validando tempo e forçando re-alocação segura. """
        if not force and not agendamento.pode_cancelar:
            raise ValidationError('Status não permite reagendar (deve estar Agendado ou Confirmado).')
            
        valido_futuro, err_fut = AgendamentoValidator.validar_data_hora_futura(nova_data_hora)
        if not valido_futuro:
            raise ValidationError(err_fut)
        
        # Verificar conflito de pet no novo horário (ignorando o próprio agendamento)
        pet = agendamento.pet
        servico = agendamento.servico
        duracao_real = AgendamentoService.obter_duracao_servico(servico, pet)
        if AgendamentoRepository.verificar_conflito_pet(
            pet.id, nova_data_hora, duracao_real, agendamento_ignorado_id=agendamento.id
        ):
            raise ValidationError('Este pet já possui um agendamento neste horário.')
            
        data_anterior = agendamento.data_hora
        novo_funcionario = AgendamentoService._alocar_funcionario(
            nova_data_hora, 
            servico,
            pet=pet,
            agendamento_ignorado_id=agendamento.id
        )
        if not novo_funcionario:
            raise ValidationError('Novo horário indisponível para equipe ou fora da grade funcional.')
            
        agendamento.data_hora = nova_data_hora
        agendamento.funcionario = novo_funcionario
        agendamento.duracao_real = duracao_real
        agendamento.status = Agendamento.Status.AGENDADO

        # Atualizar forma de pagamento se informada
        if forma_pagamento_id:
            from apps.pagamentos.models import FormaPagamento
            try:
                forma = FormaPagamento.objects.get(id=forma_pagamento_id)
                agendamento.forma_pagamento = forma
            except FormaPagamento.DoesNotExist:
                raise ValidationError('Forma de pagamento não encontrada.')

        agendamento.save()

        # Auditoria — rastreabilidade de reagendamentos
        AuditLogger.log_agendamento_reagendado(agendamento, data_anterior)
        
=======
    def reagendar(agendamento, nova_data_hora):
        """
        Reagenda um agendamento.
        """
        if not agendamento.pode_cancelar:
            raise ValidationError('Este agendamento não pode ser reagendado.')
        
        # Verificar disponibilidade do novo horário
        if not AgendamentoService.verificar_disponibilidade(
            nova_data_hora, agendamento.servico.duracao_minutos
        ):
            raise ValidationError('Novo horário indisponível.')
        
        # Atualizar agendamento
        agendamento.data_hora = nova_data_hora
        agendamento.status = Agendamento.Status.AGENDADO
        agendamento.save()
        
        # Enviar notificação de reagendamento
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        try:
            from apps.notificacoes.services import NotificacaoService
            NotificacaoService.enviar_reagendamento(agendamento)
        except ImportError:
            pass
<<<<<<< HEAD
            
=======
        
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        return agendamento
    
    @staticmethod
    def iniciar_agendamento(agendamento, funcionario):
<<<<<<< HEAD
        """ Action interna dos Vets """
        if not agendamento.pode_iniciar:
            raise ValidationError('Status do Agendamento não permite inicia-lo.')
            
        agendamento.status = Agendamento.Status.EM_ANDAMENTO
        agendamento.funcionario = funcionario
        agendamento.save()
=======
        """
        Inicia um agendamento (muda status para EM_ANDAMENTO).
        """
        if not agendamento.pode_iniciar:
            raise ValidationError('Este agendamento não pode ser iniciado.')
        
        agendamento.status = Agendamento.Status.EM_ANDAMENTO
        agendamento.funcionario = funcionario
        agendamento.save()
        
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
        return agendamento
    
    @staticmethod
    @transaction.atomic
<<<<<<< HEAD
    def concluir_agendamento(agendamento, observacoes='', valor_pago=None, forma_pagamento_id=None):
        if not agendamento.pode_concluir:
            raise ValidationError('Este agendamento não pode ser concluído.')

        # Atualiza forma de pagamento se informada
        if forma_pagamento_id:
            from apps.pagamentos.models import FormaPagamento
            try:
                agendamento.forma_pagamento = FormaPagamento.objects.get(id=forma_pagamento_id)
            except FormaPagamento.DoesNotExist:
                pass

        agendamento.status = Agendamento.Status.CONCLUIDO
        agendamento.status_pagamento = Agendamento.StatusPagamento.PAGO
        if valor_pago is not None:
            agendamento.valor_pago = valor_pago
        else:
            agendamento.valor_pago = agendamento.servico.preco
        if observacoes:
            agendamento.observacoes += f'\n{observacoes}'
        agendamento.save()

        # Auditoria — rastreabilidade finânceira
        AuditLogger.log_agendamento_concluido(agendamento, valor_pago)
        
        # Histórico
        try:
            from apps.historico.models import HistoricoAtendimento
            
            v_pago = valor_pago if valor_pago is not None else agendamento.servico.preco
=======
    def concluir_agendamento(agendamento, observacoes='', valor_pago=None):
        """
        Conclui um agendamento e cria registro no histórico.
        """
        if not agendamento.pode_concluir:
            raise ValidationError('Este agendamento não pode ser concluído.')
        
        # Atualizar agendamento
        agendamento.status = Agendamento.Status.CONCLUIDO
        if observacoes:
            agendamento.observacoes += f'\n{observacoes}'
        agendamento.save()
        
        # Criar registro no histórico (UC15)
        try:
            from apps.historico.models import HistoricoAtendimento
            from django.utils import timezone
            
            # Usar valor do serviço se não fornecido
            if valor_pago is None:
                valor_pago = agendamento.servico.preco
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
            
            HistoricoAtendimento.objects.get_or_create(
                agendamento=agendamento,
                defaults={
                    'pet': agendamento.pet,
                    'forma_pagamento': agendamento.forma_pagamento,
                    'data_atendimento': timezone.now(),
                    'tipo_servico': agendamento.servico.tipo,
                    'observacoes': observacoes,
<<<<<<< HEAD
                    'valor_pago': v_pago
                }
            )
        except ImportError:
            pass
            
        return agendamento
=======
                    'valor_pago': valor_pago
                }
            )
        except ImportError:
            pass  # Modelo ainda não existe
        
        return agendamento

>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
