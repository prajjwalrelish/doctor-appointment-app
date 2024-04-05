from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import DoctorProfile, User
from django.utils.encoding import  force_str
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

class UserProfileSerializer(DynamicFieldsMixin ,serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


    def create(self, validated_data):
        """
        Create user instance
        Set password for the user
        Return user instance
        """
        # validated_data["email"] = validated_data["username"]
        user = User.objects.create_user(**validated_data)
        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', status=status.HTTP_401_UNAUTHORIZED)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is not matched invalid', status=status.HTTP_401_UNAUTHORIZED)
        return super().validate(attrs)


class DoctorProfileSerializer(DynamicFieldsMixin ,serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'invalid_token': ('Token is expired or invalid, Please regenerate it')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')