from rest_framework import serializers

from .models import Transactions, Seminar

class TransactionSerializer(serializers.ModelSerializer):
    # payment_id = serializers.CharField(max_length=100)
    class Meta:
        model = Transactions
        fields = "__all__"
        


class SeminarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seminar
        fields = "__all__"