import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path
from string import Template


# sqtelatkjstoxwjs
def send_template_email(recipient, subject, template, variables):
    email = MIMEMultipart()
    email["From"] = "Pulsar Inc <pulsarinc.app@gmail.com>"
    email["To"] = recipient
    email["Date"] = formatdate(localtime=True)
    email["Subject"] = subject

    template = Template(Path(f"pulsar/templates/{template}.html").read_text())
    body = template.substitute(variables)

    email.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL(
        "smtp.gmail.com", 465, context=ssl.create_default_context()
    ) as server:
        server.login("pulsarinc.app@gmail.com", "sqtelatkjstoxwjs")
        res = server.sendmail(email["From"], email["To"], email.as_string())
        print(res)
