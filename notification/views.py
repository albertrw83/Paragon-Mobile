import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from tracker.models import Equipment, UserEquipment
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notifications.html'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(user=self.request.user)


def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notification_{request.user.id}',
        {
            'type': 'notification_message',
            'message': json.dumps({
                    'count': request.user.user.unread_notification().count()
                })
        }
    )
    return HttpResponse('Done')


class ToggleEquipmentNotification(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        equipment_id = kwargs.get('equipment_id')

        user_equipment, _ = UserEquipment.objects.get_or_create(
            equipment_id=equipment_id, user=self.request.user.user
        )
        if user_equipment.get_notification:
            user_equipment.get_notification = False
        else:
            user_equipment.get_notification = True
        user_equipment.save()
        data = {
            'error': False,
            'get_notification': user_equipment.get_notification
        }

        return JsonResponse(data)


class ToggleGeneralNotification(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        if self.request.user.user.get_notification:
            self.request.user.user.get_notification = False
        else:
            self.request.user.user.get_notification = True
        self.request.user.user.save()
        data = {
            'error': False,
            'get_notification': self.request.user.user.get_notification
        }

        return JsonResponse(data)


class NotificationDetail(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'notification/notification.html'

    def dispatch(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')
        note = Notification.objects.get(id=notification_id)
        if request.user.is_superuser or request.user == note.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get(self, *args, **kwargs):
        # updated the state of the notification after it is opened
        notification_id = kwargs.get('pk')
        Notification.objects.filter(id=notification_id).update(read=True)
        return super().get(*args, **kwargs)
