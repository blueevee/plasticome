import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from plasticome.config.celery_config import celery_app


@celery_app.task
def send_email_with_results(result, user_email, user_name):
    if result[1]:
        print('DEU ERRO NA TASK ANTERIOR', result)

    smtp_server = os.getenv('MAIL_SERVER')
    smtp_port = os.getenv('MAIL_PORT')
    smtp_username = os.getenv('MAIL_SENDER')
    smtp_password = os.getenv('MAIL_PASS')

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = user_email
    msg['Subject'] = '🍄 PLASTICOME: Resultados da análise'

    body = f'Olá {user_name}, segue anexo do resultado da sua análise de proteínas via plasticome.'
    msg.attach(MIMEText(body, 'plain'))

    for root, _, files in os.walk(result[0]):
        for file in files:
            file_path = os.path.join(root, file)
            attachment = open(file_path, 'rb').read()
            part = MIMEApplication(attachment)
            part.set_payload(open(file_path, 'rb').read())
            part.add_header(
                'Content-Disposition', f'attachment; filename={file}'
            )
            msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(smtp_username, user_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        return False, f'Erro ao enviar e-mail: {e}'
