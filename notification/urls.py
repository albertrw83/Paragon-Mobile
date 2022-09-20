from django.urls import path

from notification.views import (NotificationListView, ToggleEquipmentNotification, ToggleGeneralNotification,
                                NotificationDetail, test)

app_name = 'notification'

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('<int:pk>/', NotificationDetail.as_view(), name='notification'),
    path('equipment/<equipment_id>/', ToggleEquipmentNotification.as_view(), name='toggle-equipment-notification'),
    path('me/', ToggleGeneralNotification.as_view(), name='toggle-my-notification'),
    path('test/', test)
]
