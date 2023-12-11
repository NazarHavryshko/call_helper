from django.urls import path, include
from rest_framework.routers import DefaultRouter

from breaks.views import dicts

route = DefaultRouter()

route.register(r'dicts/statuses/replacements', dicts.ReplacementStatusView,
               'replacement-status')
route.register(r'dicts/statuses/breaks', dicts.BreakStatusView, 'break-status')


urlpatterns = [

]

urlpatterns += path('breaks/', include(route.urls)),
