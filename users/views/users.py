from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from common.views.mixins import ListViewSet
from users.permissions import IsNotCorporate
from users.serializars.api import users as user_s
from users.serializars.api.users import UserSearchListSerializer

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
    serializer_class = user_s.ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary='Профіль користувача', tags=['Користувачі']),
    patch=extend_schema(summary='Змінити частично профіль користувача', tags=['Користувачі']),
)
class MeView(generics.RetrieveUpdateAPIView):
    pagination_class = [IsNotCorporate]
    queryset = User.objects.all()
    http_method_names = ('get', 'patch')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return user_s.MeUpdateSerializer

        return user_s.MeSerializer

    def get_object(self):
        return self.request.user


@extend_schema_view(
    list=extend_schema(summary='Список користувачів', tags=['Словники']),
)
class UserSearchListView(ListViewSet):
    # Видалити з списку супер юзера
    queryset = User.objects.exclude()
    serializer_class = UserSearchListSerializer
