from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import load_meter




class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = load_meter
        fields = ('id','meter','ksh','token','units','day','time')
