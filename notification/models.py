from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

User = get_user_model()


class Notification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    note = models.TextField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f'{self.id} | {self.user.first_name} {self.user.last_name} | notification'

    @property
    def get_absolute_url(self):
        return reverse('notification:notification', args=[self.id])
