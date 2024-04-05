from rest_framework import serializers

from .models import Questions, UserMentalHealth, QuestionList

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"


class UserMentalHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMentalHealth
        fields = "__all__"

class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionList
        fields = "__all__"