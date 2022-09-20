from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from notification.models import Notification


def send_notification_email(notification: Notification):
    subject = notification.verb

    ctx = {
        'notification': notification
    }
    body = render_to_string(
        'email/notification.html',
        ctx
    )
    email = EmailMessage(
        subject,
        body,
        to=[notification.user.email]
    )
    email.content_subtype = 'html'
    email.send()
