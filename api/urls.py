from django.urls import path, include

from api.spectacular.urls import urlpatterns as spec_urls

app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += spec_urls
