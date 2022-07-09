from django import forms

from cashback.models import Check


class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ('fiscal',)
