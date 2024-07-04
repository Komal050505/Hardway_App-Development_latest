import smtplib
import ssl
from app_development.email_setup.email_config import *

sender = SENDER_EMAIL
receivers = RECEIVER_EMAIL
message = MESSAGE
context = ssl.create_default_context()


def send_email(too_email=None, email_body=""):
    """
    This function is used to send emails when ever there is changes in CRUD operations
    :param too_email: list of email addresses needed to be sent
    :param email_body: The message which user needs to be notified
    :return: None
    """
    if too_email is None:
        too_email = []
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(sender, PASSWORD)
        server.sendmail(sender, too_email, email_body)
