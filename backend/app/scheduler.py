from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from backend.app.database import SessionLocal
from backend.app.models.agendamento import Agendamento
from backend.app.models.barbeiro import Barbeiro
from backend.app.models.cliente import Cliente
from backend.app.services.email_service import email_lembrete_agendamento
from backend.app.logger import logger


def verificar_lembretes():
    logger.info("Verificando agendamentos para lembrete...")
    db = SessionLocal()

    try:
        agora = datetime.now()
        em_uma_hora = agora + timedelta(hours=1)

        # Janela de 2 minutos para garantir que não perde
        inicio_janela = em_uma_hora - timedelta(minutes=2)
        fim_janela = em_uma_hora + timedelta(minutes=2)

        logger.info(f"Janela de verificacao: {inicio_janela} ate {fim_janela}")

        agendamentos = db.query(Agendamento).filter(
            Agendamento.status == "confirmado",
            Agendamento.data_hora >= inicio_janela,
            Agendamento.data_hora <= fim_janela
        ).all()

        logger.info(f"Agendamentos encontrados na janela: {len(agendamentos)}")

        if not agendamentos:
            return

        for agendamento in agendamentos:
            logger.info(f"Processando lembrete para agendamento id: {agendamento.id}, data_hora: {agendamento.data_hora}")

            barbeiro = db.query(Barbeiro).filter(
                Barbeiro.id == agendamento.barbeiro_id
            ).first()

            cliente = db.query(Cliente).filter(
                Cliente.id == agendamento.cliente_id
            ).first()

            if barbeiro and cliente and cliente.email:
                data_formatada = agendamento.data_hora.strftime("%d/%m/%Y às %H:%M")
                resultado = email_lembrete_agendamento(
                    destinatario=cliente.email,
                    nome_cliente=cliente.nome,
                    nome_barbeiro=barbeiro.nome,
                    data_hora=data_formatada
                )
                if resultado:
                    logger.info(f"Lembrete enviado com sucesso para: {cliente.email}")
                else:
                    logger.error(f"Falha ao enviar lembrete para: {cliente.email}")
            else:
                logger.warning(f"Cliente sem email - agendamento id: {agendamento.id}")

    except Exception as e:
        logger.error(f"Erro ao verificar lembretes: {str(e)}")
    finally:
        db.close()


def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        verificar_lembretes,
        "interval",
        minutes=1,
        id="lembrete_agendamentos"
    )
    scheduler.start()
    logger.info("Scheduler de lembretes iniciado!")
    return scheduler