from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views as userview
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Transactionhistory',userview.TransactionView,'Transactionhistory')

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('index/', userview.index, name='index'),
    path('chart/', userview.ChartView.as_view(), name='mycharts'),
    path('api/chart_data/', userview.chart_data.as_view(), name='chart_api'),
    path('transaction/', userview.ConsumptionListView.as_view(), name='transaction'),
    path('api/transaction_data/', userview.momo.as_view(), name='transaction_api'),
    path('api/',include(router.urls)),
]

