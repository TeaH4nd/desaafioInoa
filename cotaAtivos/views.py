from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AcaoForm
import yfinance as yf
from .models import Acao

def index(request):
    return render(request, 'index.html', {})

def home(request):
    import requests
    #import json 

    if request.method == 'POST':
        simbolo = request.POST['simbolo']

        #api_request = requests.get("https://api.hgbrasil.com/finance/stock_price?key=a5508924&symbol={}".format(simbolo))

        try:
            api_request = yf.Ticker(simbolo)
        except Exception as e:
            api_request = 200

        #apiList = list(api['results'].values())
        return render(request, 'home.html', {'api':api_request.info})
    else:
        return render(request, 'home.html', {'simbolo':"Digite um simbolo acima para pesquisa"})


def portifolio(request):
    import requests

    if request.method == 'POST':
        form = AcaoForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Adicionado com Sucesso!"))
            return redirect('portifolio')
    else:    
        simbolo = Acao.objects.all()
        acoes = []
        for item in simbolo:
            #print(item.id)
            try:
                api_request = yf.Ticker(str(item))
                api_request.info["id"] = item.id
                acoes.append(api_request.info)
            except Exception as e:
                api_request = 200

        return render(request, 'portifolio.html', {'simbolo':simbolo, 'lista':acoes})

def delete(request, acao_id):
    item = Acao.objects.get(pk=acao_id)
    item.delete()
    messages.success(request, ("Deletado com Sucesso!"))
    return redirect('portifolio')