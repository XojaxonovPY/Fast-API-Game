import smtplib
from email.message import EmailMessage
from celery import Celery
from utils.settings import Settings

app = Celery('apps', broker=Settings.REDIS_URL)


@app.task
def send_email_code(to_email: dict, content: str):
    message = EmailMessage()
    message["From"] = Settings.EMAIL_FROM
    message["To"] = to_email.get('email')
    message["Subject"] = 'Tasdiqlash kodi'
    message.set_content(str(content))

    with smtplib.SMTP(Settings.SMTP_HOST, Settings.SMTP_PORT) as server:
        server.starttls()
        server.login(Settings.EMAIL_FROM, Settings.EMAIL_PASSWORD)
        server.send_message(message)
    return "Success"
