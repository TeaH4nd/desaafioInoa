from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AcaoForm
import yfinance as yf
from .models import Acao, Salvo

def index(request):
    return render(request, 'index.html', {})

def home(request):
    import requests
    #import json 

    if request.method == 'POST':
        simbolo = request.POST['simbolo']
        #print(simbolo)
        #api_request = requests.get("https://api.hgbrasil.com/finance/stock_price?key=a5508924&symbol={}".format(simbolo))

        try:
            api_request = yf.Ticker(simbolo)
            #print(api_request)
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

        try:
            api_request = yf.Ticker(simbolo)
        except Exception as e:
            api_request = 200

        if (form.is_valid()) and (api_request != 200):
            form.save()
            messages.success(request, ("Adicionado com Sucesso!"))
            return redirect('portifolio')
        else:
            messages.error(request, ("Ação não encontrada."))
            return redirect('portifolio')
    else:    
        acoes = Salvo.objects.all()
        listAcoes = []
        for item in acoes:
            dictAcoes = {}
            dictAcoes["id"] = getattr(item, "id")
            dictAcoes["symbol"] = getattr(item, "simbolo")
            dictAcoes["regularMarketPrice"] = getattr(item, "preco")
            dictAcoes["dayHigh"] = getattr(item, "alta")
            dictAcoes["dayLow"] = getattr(item, "baixa")
            dictAcoes["previousClose"] = getattr(item, "fechAnt")
            dictAcoes["marketCap"] = getattr(item, "capMerc")
            dictAcoes["longName"] = getattr(item, "nome")
            dictAcoes["data"] = getattr(item, "data")
            #print(getattr(item, "data"))

            listAcoes.append(dictAcoes)
        return render(request, 'portifolio.html', {'lista':listAcoes})

def delete(request, acao_id):
    item = Acao.objects.get(pk=acao_id)
    item.delete()
    messages.success(request, ("Deletado com Sucesso!"))
    return redirect('portifolio')

def atualizar(request):
    simbolo = Acao.objects.all()
    acoes = []
    salvo = []
    for item in simbolo:
        #print(item.id)
        try:
            api_request = yf.Ticker(str(item))
            api_request.info["id"] = item.id
            acoes.append(api_request.info)
        except Exception as e:
            api_request = 200
    Salvo.objects.all().delete()
    for item in acoes:
        s = Salvo()
        s.id = item["id"]
        s.nome = item["longName"]
        s.simbolo = item["symbol"]
        s.preco = item["regularMarketPrice"]
        s.alta = item["dayHigh"]
        s.baixa = item["dayLow"]
        s.fechAnt = item["previousClose"]
        s.capMerc = item["marketCap"]
        #print(item["longName"])

        s.save()
        
    #print(Salvo.objects.all())
    return render(request, 'portifolio.html', {'lista':acoes})