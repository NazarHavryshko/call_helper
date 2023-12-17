from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.mixins import ExtendedModelSerializer
from organizations.constants import DIRECTOR_POSITION
from organizations.models.organizations import Organization
from users.serializars.nested.users import UserShortSerializer

User = get_user_model()


class OrganizationSearchListSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'director',
        )


class OrganizationListSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()
    pax = serializers.IntegerField()
    groups_count = serializers.IntegerField()
    can_manage = serializers.BooleanField()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'director',
            'pax',
            'groups_count',
            'created_at',
            'can_manage',
        )


class OrganizationRetrieveSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()
    pax = serializers.IntegerField()
    groups_count = serializers.IntegerField()
    can_manage = serializers.BooleanField()

    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'director',
            'pax',
            'groups_count',
            'created_at',
            'can_manage',
        )


class OrganizationCreateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name'
        )

    def validate_name(self, value):
        if self.Meta.model.objects.filter(name=value):
            raise ParseError(
                'Організація з таким іменем уже існкує'
            )

        return value

    def validate(self, attrs):
        user = get_current_user()
        attrs['director'] = user
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            instance.employees.add(
                validated_data['director'],
                through_defaults={'position_id': DIRECTOR_POSITION, }

            )

        return instance


class OrganizationUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name'
        )



