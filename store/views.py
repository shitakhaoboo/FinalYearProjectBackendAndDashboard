from django.shortcuts import render
from .models import Meter,load_meter, daily_consumption
from django.contrib.auth.models import  User
from django.views.generic import ListView, View
from django.http import  JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django_tables2 import SingleTableView
from .transaction_table import TrasnactionTable
from rest_framework import viewsets,permissions
from .serializers import TransactionSerializer, ConsumptionSerializer

def index(request):
    # #to get the current logged_in user
    # user = User.objects.get(username=request.user.username)
    # #to get the balance of the current logged -in user
    # p = Meter.objects.get(user_id_id__exact=user.id)
    # context = {
    #     'Meter': p.balance
    # }
    return render(request, 'store/index.html')


class PostListView(ListView):
    model = Meter
    template_name = 'store/index.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'Meter'

'''def register_Client(request):
    if(request.user.is_authenticated):
        ExampleFormSet = modelform_factory(Client_data, fields=('f_name', 'l_name', 'username', 'password'))
        form = ExampleFormSet()
        if request.method == 'POST':
            form = ExampleFormSet(request.POST)
            # instances = form.save(commit=False)
            # for instance in instances:
            #   instance.save()
            instances = form.save()
        messages.success(request, 'Client added successfully')
        return render(request, 'store/register_client.html', {'form': form})
    else:
        messages.error(request, 'Failed request! Please log in first')
        return HttpResponseRedirect('/../../login')'''

class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'store/charts.html',{})


def get_data(request, *args, **kwargs):
    data = {
        "sales": 1000,
        "customer": 4000,
    }
    return JsonResponse(data)


class chart_data(APIView):


    def get(self, request, format=None):
        user = User.objects.get(username=request.user.username)
        p = Meter.objects.get(user_id_id__exact=user.id)
        m = daily_consumption.objects.values('usage').filter(meter_id=p.id)
        m1 = [entry for entry in m]
        m3 = daily_consumption.objects.values('day')
        #m4 = [entry for entry in m3]
        labels = [d['day'] for d in m3]
        default_items = [d['usage'] for d in m1]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)



class momo(APIView):
    #to fetch details of user's meter number and account number


    def get(self, request, format=None):
        user = User.objects.get(username=request.user.username)
        lala = Meter.objects.get(user_id_id__exact=user.id)
        data = {
            "labels": lala.meter_number,
            "default":lala.account_number,
        }
        return Response(data)


class ConsumptionListView(SingleTableView):
    model = load_meter
    table_class = TrasnactionTable
    template_name = 'store/transaction.html'
    
    
class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = load_meter.objects.all()

    
class ConsumptionView(viewsets.ModelViewSet):
    serializer_class = ConsumptionSerializer
    queryset = daily_consumption.objects.all()
