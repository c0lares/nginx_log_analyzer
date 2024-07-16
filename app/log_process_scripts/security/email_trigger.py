import smtplib
from smtplib import SMTPAuthenticationError
from email.message import EmailMessage
from config import logging, EMAIL_SENDER, EMAILS_ADMINS, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER


def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(body)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAILS_ADMINS, msg.as_string())
        # s = smtplib.SMTP('smtp.gmail.com: 587')
        
        logging.info("Email enviado")
    except SMTPAuthenticationError:
        logging.critical("Nao foi possivel mandar o email, autenticacao incorreta")
    except Exception as e:
        logging.critical("Nao foi possivel enviar o email: " + str(e))
        
    
def notify_admins(report):
    subject = f"Logs suspeitos: {report['mesage_to_report']}"
    body = f"""
    <h2> Foi verificado comportamentos suspeitos no log do nginx </h2>
    <p> Mensagem: {report['mensage']} </p>
    <p> Ultima data do ocorrido: {report['last_datetime']}</p>
    """
    send_email(subject, body)