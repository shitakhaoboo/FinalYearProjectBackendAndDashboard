from django.db import models
from django.contrib.auth.models import  User
from datetime import datetime

# Create your models here.

class Meter(models.Model):

    #meter number allows one client to have many meters
    meter_number = models.CharField(max_length=20)
    account_number = models.CharField(max_length=20,default=0)
    #assuming there's a numbering strategy for housing
    user_id = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.meter_number


'''def update_balance(self, balance_read):
        #we need to receive the data sent in and store it into the databases
        self.balance = balance_read



    def load_tokens(tokens):
        balance = tokens +  
'''

class load_meter(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.PROTECT)
    units = models.FloatField(default=0)
    day = models.CharField(max_length=20)
    time = models.TimeField(auto_now_add=True)
    ksh = models.FloatField(default=0)


class daily_consumption(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.PROTECT)
    usage = models.FloatField(default=0)
    day = models.CharField(max_length=20)
