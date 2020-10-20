from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import load_meter, daily_consumption




class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = load_meter
        fields = ('id','meter','ksh','token','units','day','time')
  

class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = daily_consumption
        fields = ('id','meter','usage','day')
