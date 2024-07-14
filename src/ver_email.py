import smtplib;
import os;
import ssl;

from src.config import settings;
from pydantic.dataclasses import dataclass;

from email.mime.base import MIMEBase;
from email.mime.multipart import MIMEMultipart;
from email.mime.text import MIMEText;

SMTP_SERVER = settings.smtp_server;
SMTP_PORT = settings.smtp_port;
SMTP_EMAIL = settings.smtp_email.get_secret_value();
SMTP_PASS = settings.smtp_pass.get_secret_value();

@dataclass
class Email:
    subject:str;
    body: str;
    recipient:str;

context = ssl.create_default_context();

def email_server(email: Email):
    message = MIMEMultipart();
    message['From'] = SMTP_EMAIL;
    message['To'] = email.recipient;
    message['Subject'] = email.subject;
    message.attach(MIMEText(email.body, "plain"));
    text = message.as_string();
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context= context);
        server.login(SMTP_EMAIL, SMTP_PASS);
        server.sendmail(SMTP_EMAIL, email.recipient, text);




