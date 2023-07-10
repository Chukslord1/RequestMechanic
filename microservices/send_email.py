from django.core.mail import send_mail
from django.conf import settings


def send_email(email_to, title, content):
    try:
        send_mail(
            subject=title,
            message=content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_to],
            fail_silently=False
        )
        return True
    except Exception as e:
        return False
