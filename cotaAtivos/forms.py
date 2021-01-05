from django import forms
from .models import Acao

class AcaoForm(forms.ModelForm):
    class Meta:
        model = Acao
        fields = ["simbolo"]