from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/notification/<room_id>/', consumers.NotificationConsumer.as_asgi()),
]
