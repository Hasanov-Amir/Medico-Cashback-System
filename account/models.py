from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=False)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField()
    email_verify = models.BooleanField(default=False, verbose_name="Подтверждение аккаунта")
    conditions = models.BooleanField(default=False, verbose_name="Условия конфиденциальности")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_absolute_url(self):
        return reverse('profile', kwargs={"": self.email})
