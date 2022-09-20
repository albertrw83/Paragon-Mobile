import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.models import Notification
from notification.utils import send_notification_email


@receiver(post_save, sender=Notification)
def notification_post_save(sender, instance, created, **kwargs):

    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notification_{instance.user.id}',
            {
                'type': 'notification_message',
                'message': json.dumps({
                    'count': instance.user.user.unread_notification().count()
                })
            }
        )
        send_notification_email(instance)
