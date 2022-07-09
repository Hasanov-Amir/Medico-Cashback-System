from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.tokens import default_token_generator

from MedicoCashbackSystem import settings
from .forms import *


def index(request):
    return render(request, "home.html")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
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


@login_required(redirect_field_name='login')
def user_profile(request):
    user = auth.get_user(request)
    data = {
        'profile': user
    }
    return render(request, "account/profile.html", data)


def edit_profile(request):
    data = {}

    user = auth.get_user(request)
    profile = User.objects.get(id=user.id)
    form = EditUserForm(request.POST or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            if form.instance.email != profile.email:
                form.save()
                profile = User.objects.get(id=user.id)
                profile.email_verify = False
                profile.save()
                send_email_for_verify(request, profile)
            return redirect("profile")

    data["form"] = form
    return render(request, "account/edit_profile.html", data)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Medico',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_from = settings.EMAIL_HOST_USER
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, email_from, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password/password_reset.html",
        context={
            "password_reset_form": password_reset_form
        }
    )


def logout_user(request):
    logout(request)
    return redirect('home')


def page_not_found(request, exception):
    response = render(request, 'error404.html', {"tried": exception})
    response.status_code = 404
    return response
