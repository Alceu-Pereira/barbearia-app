import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from backend.app.logger import logger

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")


def enviar_email(destinatario: str, assunto: str, mensagem: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = destinatario
        msg["Subject"] = assunto

        msg.attach(MIMEText(mensagem, "html"))

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        servidor.quit()

        logger.info(f"Email enviado com sucesso para: {destinatario}")
        return True

    except Exception as e:
        logger.error(f"Erro ao enviar email para {destinatario}: {str(e)}")
        return False


def email_confirmacao_agendamento(
    destinatario: str,
    nome_cliente: str,
    nome_barbeiro: str,
    data_hora: str
):
    assunto = "✂️ Confirmação de Agendamento — Barbearia"
    mensagem = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a1a2e; padding: 24px; text-align: center;">
            <h1 style="color: white;">✂️ Barbearia</h1>
        </div>
        <div style="padding: 32px;">
            <h2>Olá, {nome_cliente}! 👋</h2>
            <p>Seu agendamento foi <strong>confirmado</strong> com sucesso!</p>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 24px 0;">
                <p><strong>💈 Barbeiro:</strong> {nome_barbeiro}</p>
                <p><strong>📅 Data e Hora:</strong> {data_hora}</p>
                <p><strong>📌 Status:</strong> ✅ Confirmado</p>
            </div>
            <p>Te esperamos! 😄</p>
        </div>
        <div style="background-color: #f0f2f5; padding: 16px; text-align: center;">
            <p style="color: #666; font-size: 0.85rem;">Barbearia App — Sistema de Agendamentos</p>
        </div>
    </body>
    </html>
    """
    return enviar_email(destinatario, assunto, mensagem)


def email_cancelamento_agendamento(
    destinatario: str,
    nome_cliente: str,
    nome_barbeiro: str,
    data_hora: str
):
    assunto = "❌ Agendamento Cancelado — Barbearia"
    mensagem = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a1a2e; padding: 24px; text-align: center;">
            <h1 style="color: white;">✂️ Barbearia</h1>
        </div>
        <div style="padding: 32px;">
            <h2>Olá, {nome_cliente}! 👋</h2>
            <p>Seu agendamento foi <strong>cancelado</strong>.</p>
            <div style="background-color: #f8d7da; padding: 20px; border-radius: 8px; margin: 24px 0;">
                <p><strong>💈 Barbeiro:</strong> {nome_barbeiro}</p>
                <p><strong>📅 Data e Hora:</strong> {data_hora}</p>
                <p><strong>📌 Status:</strong> ❌ Cancelado</p>
            </div>
            <p>Para fazer um novo agendamento acesse nosso sistema! 😄</p>
        </div>
        <div style="background-color: #f0f2f5; padding: 16px; text-align: center;">
            <p style="color: #666; font-size: 0.85rem;">Barbearia App — Sistema de Agendamentos</p>
        </div>
    </body>
    </html>
    """
    return enviar_email(destinatario, assunto, mensagem)


def email_lembrete_agendamento(
    destinatario: str,
    nome_cliente: str,
    nome_barbeiro: str,
    data_hora: str
):
    assunto = "⏰ Lembrete de Agendamento — Barbearia"
    mensagem = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a1a2e; padding: 24px; text-align: center;">
            <h1 style="color: white;">✂️ Barbearia</h1>
        </div>
        <div style="padding: 32px;">
            <h2>Olá, {nome_cliente}! 👋</h2>
            <p>Lembrando que você tem um agendamento em <strong>1 hora</strong>!</p>
            <div style="background-color: #fff3cd; padding: 20px; border-radius: 8px; margin: 24px 0;">
                <p><strong>💈 Barbeiro:</strong> {nome_barbeiro}</p>
                <p><strong>📅 Data e Hora:</strong> {data_hora}</p>
                <p><strong>📌 Status:</strong> ⏰ Em breve!</p>
            </div>
            <p>Te esperamos! 😄</p>
        </div>
        <div style="background-color: #f0f2f5; padding: 16px; text-align: center;">
            <p style="color: #666; font-size: 0.85rem;">Barbearia App — Sistema de Agendamentos</p>
        </div>
    </body>
    </html>
    """
    return enviar_email(destinatario, assunto, mensagem)