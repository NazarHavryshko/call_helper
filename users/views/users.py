from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.serializars.api import users as user_s

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Регістрація користувача', tags=['Аутентифікація і Авторизація']),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializer
