from celery import shared_task
from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


@shared_task
def send_email(receiver_email, code):
    subject = "Verification code"
    message = f"Code: {code}"
    send_mail(subject, message, EMAIL_HOST_USER, [receiver_email])
    return {"status": f"Successfully sent email to {receiver_email}"}