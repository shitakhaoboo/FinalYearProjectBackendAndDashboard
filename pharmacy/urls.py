"""pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from store import views as userview
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Transactionhistory',userview.TransactionView,'Transactionhistory')

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='store/login.html'),name = 'login'),
    path('login/',auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('index/',userview.index,name = 'index'),
    path('chart/',userview.ChartView.as_view(),name='mycharts'),
    path('api/chart_data/', userview.chart_data.as_view(),name='chart_api'),
    path('transaction/', userview.ConsumptionListView.as_view(),name='transaction'),
    path('api/transaction_data/',userview.momo.as_view(),name='transaction_api'),
    path('api/',include(router.urls)),
]
