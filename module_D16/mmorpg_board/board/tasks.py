from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_newsletter(subject, message):
    from django.contrib.auth.models import User
    recipients = User.objects.filter(is_active=True).values_list('email', flat=True)
    for recipient in recipients:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

@shared_task
def send_response_notification(email, post_title):
    send_mail(
        subject='Your response was accepted',
        message=f'Your response to the post "{post_title}" has been accepted.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )