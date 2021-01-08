from django import forms
from .models import Acao, Perfil

class AcaoForm(forms.ModelForm):
    class Meta:
        model = Acao
        fields = ["simbolo"]

class EmailForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["email"]

class LimiteForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["limSup", "limInf"]

class TempoForm(forms.Form):
    numero = forms.FloatField(min_value = 0)
    tempo = forms.IntegerField()