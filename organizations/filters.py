import django_filters

from organizations.models.grups import Group
from organizations.models.organizations import Organization, Employee


class OrganisationFilter(django_filters.FilterSet):
    can_manage = django_filters.BooleanFilter('can_manage', label='Can manage')

    class Meta:
        model = Organization
        fields = ('can_manage', 'id')


class EmployeeFilter(django_filters.FilterSet):
    only_corporate = django_filters.BooleanFilter(
        'user__is_corporate_account', label='Is corporate account'
    )

    class Meta:
        model = Employee
        fields = ('only_corporate', )


class GroupFilter(django_filters.FilterSet):
    is_member = django_filters.BooleanFilter('is_member')

    class Meta:
        model = Group
        fields = ('organization', 'manager', 'is_member')
