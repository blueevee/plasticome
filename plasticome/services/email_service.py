import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

from plasticome.config.celery_config import celery_app


@celery_app.task
def send_email_with_results(result, user_email, user_name):
    if result[1]:
        print('DEU ERRO NA TASK ANTERIOR', result)

    smtp_server = os.getenv('MAIL_SERVER')
    smtp_sender = os.getenv('MAIL_USER')
    smtp_password = os.getenv('MAIL_SECRET')
    smtp_port = os.getenv('MAIL_ACCESS_PORT')

    msg = MIMEMultipart()
    msg['From'] = smtp_sender
    msg['To'] = user_email
    msg['Subject'] = '[🍄 PLASTICOME]: Resultados da análise'

    body = f'Olá {user_name}, segue em anexo do resultado da sua análise de proteínas via plasticome.'
    msg.attach(MIMEText(body, 'plain'))

    for root, _, files in os.walk(result[0]):
        for file in files:
            file_path = os.path.join(root, file)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file_path, 'rb').read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition', f'attachment; filename={file}'
            )
            msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_sender, smtp_password)
        server.sendmail(smtp_sender, user_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        return False, f'Erro ao enviar e-mail: {e}'
