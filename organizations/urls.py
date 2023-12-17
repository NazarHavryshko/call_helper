from django.urls import path, include
from rest_framework.routers import DefaultRouter

from organizations.views import dicts, organizations, employee, groups

route = DefaultRouter()

route.register(r'dicts/positions', dicts.PositionView, 'positions')
route.register(r'search', organizations.OrganizationSearchListView, 'organizations-search')
route.register(r'manage', organizations.OrganizationView, 'organizations')
route.register(r'manage/(?P<id>\d+)/employees', employee.EmployeeView, 'employees')
route.register(r'group', groups.GroupView, 'group')

urlpatterns = [

]

urlpatterns += path('organizations/', include(route.urls)),
