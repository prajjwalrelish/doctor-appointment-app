from rest_framework import routers
from .views import AppointmentViewSet,UserNotificationViewSet,DoctorNotificationViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'appointment',AppointmentViewSet)
router.register(r'notification/user',UserNotificationViewSet)
router.register(r'notification/doctor',DoctorNotificationViewSet)

urlpatterns = router.urls