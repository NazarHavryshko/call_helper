from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.serializars.nested.profile import ProfileShortSerializer, \
    ProfileUpdateSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', ]

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'Користувач з такою поштою вже зареєстрований.'
            )

        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.pop('old_password')
        if not user.check_password(old_password):
            raise ParseError('Поточний пароль не вірний.')

        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('new_password')
        instance.set_password(password)
        instance.save()
        return instance


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileShortSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'phone_number',
            'profile',
            'date_joined',
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'phone_number',
            'profile',
            'date_joined',
        )

    def validate(self, attrs):
        user = self.instance
        if user.is_corporate_account:
            raise ParseError(

            )
        return attrs

    def update(self, instance, validated_data):
        # Перевірка існування профіля
        profile_data = validated_data.pop(
            'profile') if 'profile' in validated_data else None

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            # Оновлення профілю
            if profile_data:
                self._update_profile(instance.profile, profile_data)

        return instance

    def _update_profile(self, profile, data):
        profile_serializer = ProfileUpdateSerializer(
            instance=profile, data=data, partial=True)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()


class UserSearchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'full_name',
        )
