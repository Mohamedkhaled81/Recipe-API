"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate)
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # Making the password 'write_only' for not returning
        # the password in the response of the api
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        # If we didn't override the the create method password will
        # Be saved as plain text..
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Updating the user info."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class TokenSerializer(serializers.Serializer):
    """Serializer for Tokens"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
        )

    def validate(self, attrs):
        """Validating and authenticate the user"""
        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password)

        if not user:
            msg = _("Invalid Credentials")
            raise serializers.ValidationError(msg, code='authorization')

        # So we can use the user in the view
        # This is REQUIRED
        attrs['user'] = user
        return attrs
