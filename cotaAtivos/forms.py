from django import forms
from .models import Acao, Email

class AcaoForm(forms.ModelForm):
    class Meta:
        model = Acao
        fields = ["simbolo"]

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ["email"]

class TempoForm(forms.Form):
    numero = forms.FloatField(min_value = 0)
    tempo = forms.IntegerField()