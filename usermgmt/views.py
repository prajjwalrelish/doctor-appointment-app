from re import I
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import DoctorProfile, User
from .serializers import DoctorProfileSerializer, UserProfileSerializer,EmailVerificationSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer
from .permissions import AllowAnyExceptAuthenticatedListOnly
from .permissions import DeleteNotAllowed
from .permissions import IsOwnerOrAuthenticatedReadOnly
from rest_framework import viewsets
from rest_framework import status
from .serializers import LogoutSerializer
from rest_framework import generics,permissions

from rest_framework_simplejwt.tokens import RefreshToken
from .email import Email
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from livLife import settings
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.http import HttpResponsePermanentRedirect
import os

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

# from rest_framework.authtoken.models import Token
# import json
# from django.shortcuts import render
# from django.utils import timezone
# from rest_framework import serializers
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAdminUser
# from django.db import IntegrityError
# from django.contrib.auth import login, logout
# from django.core.exceptions import ValidationError
# from django.contrib.auth.hashers import check_password


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = (
        AllowAnyExceptAuthenticatedListOnly,
        IsOwnerOrAuthenticatedReadOnly,
        DeleteNotAllowed,
    )

    def create(self, request, *args, **kwargs):
        userSerializer = UserProfileSerializer(data=request.data)
        if not userSerializer.is_valid():
            return Response(data=userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        userSerializer.save()
        
        userData = userSerializer.data
        user = User.objects.get(email=userData['email'])
        token = RefreshToken.for_user(user).access_token
        currentSite = get_current_site(request).domain
        reverseLink = reverse('verify-email')
        customUrl = 'http://'+currentSite+reverseLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            'Please click the link to verify your ThreatExchange Account \n' + customUrl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Email.send_email(data)

        return Response(data=userSerializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User.objects.all(), pk=user_id)
        serializer = UserProfileSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def partial_update(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User.objects.all(), pk=user_id)

        serializer = UserProfileSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], name='current')
    def get_logged_in_user(self, request, *args, **kwargs):
        permission_classes=[IsAuthenticated]
        user_serializer = UserProfileSerializer(request.user)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=["get"], name='forgot-password')
    # def forgot_password(self, request):
    #     permission_classes=[AllowAny]
    #     email = request.GET.get("email")
    #     if not email:
    #         return Response(data="Email not present", status=status.HTTP_400_BAD_REQUEST)
    #     user = get_object_or_404(User, email=email)
        # initiate_user_email_verification(
        #     user,
        #     constants.get_forgot_password_html_payload(),
        #     constants.PAGE_SET_PASSWORD
        # )
        # return Response(status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])          
            user = User.objects.get(uuid=data['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            reverseLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirectUrl = request.data.get('redirect_url', '')
            customUrl = 'http://'+current_site + reverseLink
            email_body = 'Hi, \n Please use below mentioned URL to reset your password  \n' + \
                customUrl+"?redirect_url="+redirectUrl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Email.send_email(data)
        return Response({'success': 'We have sent you a URL to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)



class DoctorViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    serializer_class = UserProfileSerializer
    queryset = User.objects.filter(is_Doctor=True)
    permission_classes = (
        IsOwnerOrAuthenticatedReadOnly,
        DeleteNotAllowed,
    )

    def get_object(self):
        return User.objects.get(uuid=self.kwargs["uuid"])

    def list(self, request):
        queryset = User.objects.filter(is_Doctor=True)
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        

class DoctorProfileViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    serializer_class = DoctorProfileSerializer
    queryset = DoctorProfile.objects.all()
    permission_classes = (
        IsOwnerOrAuthenticatedReadOnly,
        DeleteNotAllowed,
    )
    
    def get_object(self):
        return DoctorProfile.objects.get(uuid=self.kwargs["uuid"])

    def get_queryset(self):
        return DoctorProfile.objects.filter(is_active=True)
    # def create(self, request, *args, **kwargs):
    #     user_serializer = UserProfileSerializer(data=request.data)
    #     if not user_serializer.is_valid():
    #         return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     user = user_serializer.save()
    #     return Response(data=user_serializer.data, status=status.HTTP_200_OK)
    
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def doctor_list(request):
#     doctors = User.objects.filter(is_Doctor=True)
#     serializer = UserProfileSerializer(doctors, many=True)
#     if serializer.is_valid():
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#     return Response("No Doctors")

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def Register_Users(request):
#     return Response("Authenticated")

class DoctorScheduleViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    serializer_class = UserProfileSerializer
    queryset = DoctorProfile.objects.all()
    permission_classes = (
        IsOwnerOrAuthenticatedReadOnly,
        DeleteNotAllowed,
    )

    def list (self,request):
        data = {}
        doctors = DoctorProfile.objects.all()
        serializer = DoctorProfileSerializer(doctors,many=True)
        if len(serializer.data) > 1:
            for i in range(len(serializer.data)):
                data[i] =[serializer.data[i]['doctor'], serializer.data[i]['working_hours'] ]
        print(serializer.data)
        return Response(data)

    # def retrieve(self,request,uuid):
    #     doctors = DoctorProfile.objects.get(uuid=uuid)
    #     serializer = DoctorProfileSerializer(doctors,many=True)
    #     return Response(serializer.data)


@api_view(['GET',])
def get_user_details(request, email):
    """
    get the email and return userDetail it
    """
    if request.method == 'GET':
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            serializer = UserProfileSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)