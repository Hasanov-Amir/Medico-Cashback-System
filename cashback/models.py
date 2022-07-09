from django.db import models
from django.urls import reverse

from account.models import User


class Check(models.Model):
    fiscal = models.SlugField(max_length=12, unique=True, verbose_name="Fiscal ID")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Who scanned")
    check_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sum")
    cashback_value = models.FloatField(verbose_name="Cashback value")
    on_balance = models.BooleanField(default=False, verbose_name="On Balance")
    time_added = models.DateTimeField(auto_now_add=True, verbose_name="Time Added")

    def get_absolute_url(self):
        return reverse('fiscal_show', kwargs={"fiscal": self.fiscal})

    def __str__(self):
        return f"{self.fiscal=}, {self.owner=}"
