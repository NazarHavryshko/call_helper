from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import users


route = DefaultRouter()

route.register(r'search', users.UserSearchListView, 'users-search')

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='reg'),
    path('users/me/', users.MeView.as_view(), name='me'),
    path('users/change-passwd/', users.ChangePasswordView.as_view(), name='change_passwd'),
]

urlpatterns += path('users/', include(route.urls)),
