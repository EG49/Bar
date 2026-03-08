import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_USER = "egaibor812@gmail.com"
EMAIL_PASSWORD = "hnyn vcjq bxmg evix"


def enviar_correo(destinatario, asunto, mensaje):

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        server.send_message(msg)
        server.quit()

        print("Correo enviado")

    except Exception as e:
        print("Error enviando correo:", e)