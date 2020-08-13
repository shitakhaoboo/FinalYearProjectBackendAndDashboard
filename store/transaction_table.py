import django_tables2 as tables
from .models import load_meter

class TrasnactionTable(tables.Table):
    class Meta:
        model = load_meter
        template_name = "django_tables2/bootstrap.html"
        fields = ("ksh","token","units","day","time" )
