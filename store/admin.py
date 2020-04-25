from django.contrib import admin
from .models import Meter, daily_consumption,load_meter


admin.site.register(Meter)
admin.site.register(load_meter)
admin.site.register(daily_consumption)