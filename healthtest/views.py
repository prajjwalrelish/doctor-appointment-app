from healthtest.serializers import QuestionListSerializer, QuestionSerializer,UserMentalHealthSerializer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import QuestionList, Questions, UserMentalHealth
# Create your views here.

class QuestionViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Questions.objects.get(uuid=self.kwargs["uuid"])

    def create(self, request, *args, **kwargs):
        question_serializer = QuestionSerializer(data=request.data)
        question_serializer.is_valid(raise_exception=True)
        question_serializer.save()
        question_serialized_data = question_serializer.data
        return Response(question_serialized_data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs) -> Response:
        question = self.get_object()
        serializer = QuestionSerializer(question, partial=True, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class QuestionListViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = QuestionList.objects.all()
    serializer_class = QuestionListSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['test_type']

    def get_object(self):
        return QuestionList.objects.get(uuid=self.kwargs["uuid"])

    def create(self, request, *args, **kwargs):
        question_list_serializer = QuestionListSerializer(data=request.data)
        question_list_serializer.is_valid(raise_exception=True)
        question_list_serializer.save()
        question_serialized_data = question_list_serializer.data
        return Response(question_serialized_data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs) -> Response:
        questionList = self.get_object()
        serializer = QuestionListSerializer(questionList, partial=True, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)    

class UserMentalHealthViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = UserMentalHealth.objects.all()
    serializer_class = UserMentalHealthSerializer
    