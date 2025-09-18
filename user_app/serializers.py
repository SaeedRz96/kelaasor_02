from rest_framework.serializers import ModelSerializer
from user_app.models import LoanRequest

class LoanRequestSerializer(ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ['owner', 'amount', 'months']