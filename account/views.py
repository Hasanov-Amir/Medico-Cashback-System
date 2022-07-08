from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.tokens import default_token_generator
from .forms import *


def index(request):
    return render(request, "home.html")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        # return redirect('home')
        send_email_for_verify(self.request, user)
        return redirect('confirm_email')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user