from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.models import User
from cashback.forms import CheckForm
from cashback.models import Check

import json
import requests


def check_info(info):
    return json.loads(info.content)


class CB_Add(LoginRequiredMixin, CreateView):
    form_class = CheckForm
    template_name = 'cashback/fiscal_add.html'
    login_url = reverse_lazy('home')
    raise_exception = True

    def form_valid(self, form):
        url = f'https://monitoring.e-kassa.gov.az/pks-portal/1.0.0/documents/{form.instance.fiscal}'
        page = requests.get(url)
        check_data = check_info(page)
        check_sum = check_data['cheque']['content']['sum']
        form.instance.check_sum = check_sum
        form.instance.cashback_value = check_sum*0.03
        form.instance.owner = self.request.user
        return super().form_valid(form)


def show_fiscal(request, fiscal):
    check = get_object_or_404(Check, fiscal=fiscal)
    data = {
        'check': check
    }
    return render(request, 'cashback/fiscal_show.html', data)


def history_fiscal(request):
    user = User.objects.get(id=request.user.id)
    history = user.check_set.all()
    data = {
        'history': history
    }
    return render(request, 'cashback/fiscal_history.html', data)