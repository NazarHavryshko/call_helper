from django.urls import path, include
from rest_framework.routers import DefaultRouter

from organizations.views import dicts

route = DefaultRouter()

route.register(r'dicts/positions', dicts.PositionView, 'positions')


urlpatterns = [
    path('organizations/', include(route.urls)),
]

urlpatterns += path('organizations/', include(route.urls)),
