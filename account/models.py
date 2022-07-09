from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=False)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(verbose_name="Phone")
    email_verify = models.BooleanField(default=False, verbose_name="Account Verify")
    conditions = models.BooleanField(default=False, verbose_name="Privacy Policy")
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Balance")
    pending = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Pending")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_absolute_url(self):
        return reverse('profile', kwargs={"": self.email})
