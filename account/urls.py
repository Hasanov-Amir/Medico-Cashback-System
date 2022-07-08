from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='reg'),
    path('confirm-email/', TemplateView.as_view(template_name='account/email_confirm.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),

]
