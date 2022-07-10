from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/add_card', ..., name='add_card'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='reg'),
    path('confirm_email/', TemplateView.as_view(template_name='account/email_confirm.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='account/invalid_verify.html'), name='invalid_verify'),
]
