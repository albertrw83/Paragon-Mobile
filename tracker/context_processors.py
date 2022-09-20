from django.contrib.auth.models import User
from .models import UserProperties, Company


def user_properties(request):
    try:
        user_properties=UserProperties.objects.get(user=request.user)
    except:
        user_properties=None
    return {"user_properties": user_properties}