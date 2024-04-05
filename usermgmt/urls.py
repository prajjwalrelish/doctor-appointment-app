from rest_framework import routers
from django.urls import reverse, path
from .views import UserProfileViewSet, DoctorViewSet, DoctorProfileViewSet,DoctorScheduleViewset,VerifyEmail,RequestPasswordResetEmail,PasswordTokenCheckAPI,SetNewPasswordAPIView
from .views import get_user_details
from django.conf.urls import url

# from .views import Register_Users, doctor_list, getDoctor

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'userprofile', UserProfileViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'doctor', DoctorProfileViewSet)
router.register(r'getDoctorSchedule', DoctorScheduleViewset,basename='getdoctorschedule')

urlpatterns = router.urls

urlpatterns += [
    path('getUserDetail/<email>', get_user_details, name='getUserDetail'),
    path('verify-email/', VerifyEmail.as_view(), name="verify-email"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    # url(r'^r', Register_Users, name='register'),
    # url(r'^doctors', doctor_list, name='doctor'),
    # url(r'users/(?P<doctor_id>{regex}).format(regex=UUID_REGEX)', getDoctor, name='getDoctor')
]