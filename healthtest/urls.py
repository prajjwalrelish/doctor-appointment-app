from rest_framework import routers
from django.urls import reverse
from .views import QuestionViewSet,QuestionListViewSet,UserMentalHealthViewSet
from django.conf.urls import url

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'questions', QuestionViewSet)
router.register(r'questionlist', QuestionListViewSet)
router.register(r'usertest', UserMentalHealthViewSet)

urlpatterns = router.urls

urlpatterns += [
]