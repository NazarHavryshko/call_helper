from crum import get_current_user
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import ExtendedModelSerializer
from organizations.models.grups import Group
from organizations.models.organizations import Organization
from organizations.serializars.nested.employees import EmployeeShortSerializer
from organizations.serializars.nested.organizations import OrganisationShortSerializer
from users.serializars.nested.users import UserShortSerializer

User = get_user_model()


class GroupListSerializer(ExtendedModelSerializer):
    organization = OrganisationShortSerializer()
    manager = EmployeeShortSerializer()
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'manager',
            'organization',
            'pax',
            'created_at',
            'can_manage',
            'is_member',
        )


class GroupRetrieveSerializer(ExtendedModelSerializer):
    organization = OrganisationShortSerializer()
    manager = EmployeeShortSerializer()
    pax = serializers.IntegerField()
    can_manage = serializers.BooleanField()
    is_member = serializers.BooleanField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'manager',
            'organization',
            'pax',
            'created_at',
            'can_manage',
            'is_member',
        )


class GroupCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'organization',
            'manager',
            'name',
        )

    def validate_organization(self, value):
        user = get_current_user()
        if value not in Organization.objects.filter(director=user,):
            raise ParseError(
                'Некоректно вибрана організація'
            )

        return value

    def validate(self, attrs):
        org = attrs['organization']

        # Specified manager or organization director
        attrs['manager'] = attrs.get('manager') or org.director_employee
        manager = attrs['manager']
        # Check manager
        i = org.employees_info.all()
        if manager not in org.employees_info.all():
            raise ParseError(
                'Адміністратором може бути тільки робітник організації або засновник.'
            )

        # Check name duplicate
        if self.Meta.model.objects.filter(
            organization=org, name=attrs['name']
        ).exists():
            raise ParseError(
                'Нрупа з таким іменем уже існує'
            )

        return attrs


class GroupUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )




