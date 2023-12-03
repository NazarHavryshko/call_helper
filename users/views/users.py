from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from users.serializars.api import users as user_s

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Регістрація користувача', tags=['Аутентифікація і Авторизація']),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(request=user_s.ChangePasswordSerializer,
                       summary='Зміна паролю', tags=['Аутентифікація і Авторизація']),
)
class ChangePasswordView(APIView):

    def post(self, requests):
        user = requests.user
        serializer = user_s.ChangePasswordSerializer(
            instance=user, data=requests.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary='Профіль користувача', tags=['Користувачі']),
    put=extend_schema(summary='Змінити профіль користувача', tags=['Користувачі']),
    patch=extend_schema(summary='Змінити частично профіль користувача', tags=['Користувачі']),
)
class MeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    http_method_names = ('get', 'patch')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return user_s.MeUpdateSerializer

        return user_s.MeSerializer

    def get_object(self):
        return self.request.user
