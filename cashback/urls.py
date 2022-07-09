from django.urls import path
from .views import *

urlpatterns = [
    path('add/', CB_Add.as_view(), name='fiscal_add'),
    path('show/<slug:fiscal>/', show_fiscal, name='fiscal_show'),
    path('history/', history_fiscal, name='fiscal_history'),
]
