from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import AcaoForm, EmailForm, TempoForm
from .models import Acao, Preco, Salvo, Email

import yfinance as yf
from yahoo_fin.stock_info import get_quote_table
from background_task import background
from background_task.models import CompletedTask, Task

import os

REPEAT_TIME = 60

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
            api_request = 500

        if (form.is_valid()) and (api_request != 500):
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

def acao(request, acao_id):
    precos = Preco.objects.filter(simbolo=acao_id).order_by('-data')
    acao = Salvo.objects.get(pk=acao_id)
    nome = getattr(acao, "nome")
    listPrecos = []
    for preco in precos:
        dictPreco = {}
        dictPreco["preco"] = getattr(preco, "preco")
        dictPreco["data"] = getattr(preco, "data")
        listPrecos.append(dictPreco)
    return render(request, 'acao.html', {'lista':listPrecos, "acao":nome})

def perfil(request):
    if request.method == 'POST':
        form = EmailForm(request.POST or None)
        if (form.is_valid()):
            form.save()
            messages.success(request, ("Adicionado com Sucesso!"))
            return redirect('perfil')
        else:
            messages.error(request, ("Houve um erro ao adicionar o email. O email ja esta adicionado?"))
            return redirect('perfil')
    else:
        e = Email.objects.all()
        email = []
        for item in e:
            email.append(getattr(item, "email"))
        return render(request, 'perfil.html', {"lista":email})


@background(schedule=5)
def get_precos():
    acoes = Acao.objects.all()
    for acao in acoes:
        try:
            print(str(acao))
            preco = get_quote_table(str(acao))
            #print(api_request.info["regularMarketPrice"])
            p = acao.preco_set.create(preco = preco["Quote Price"])
            p.save()
        except Exception as e:
            #print("Error")
            pass

def start_get_precos(request):
    if request.method == 'POST':
        form = TempoForm(request.POST or None)
        if (form.is_valid()):
            numero = form.cleaned_data['numero']
            tempo = form.cleaned_data['tempo']
            if tempo == 1:
                try:
                    CompletedTask.objects.all().delete()
                    Task.objects.all().delete()
                    get_precos(repeat= (numero))
                    os.system('python manage.py process_tasks')
                    return redirect('perfil')
                except Exception as e:
                    return redirect('perfil')
            elif tempo == 2:
                try:
                    CompletedTask.objects.all().delete()
                    Task.objects.all().delete()
                    get_precos(repeat= (numero*60))
                    os.system('python manage.py process_tasks')
                    return redirect('perfil')
                except Exception as e:
                    return redirect('perfil')
            elif tempo == 3:
                try:
                    CompletedTask.objects.all().delete()
                    Task.objects.all().delete()
                    get_precos(repeat= (numero*60*60))
                    os.system('python manage.py process_tasks')
                    return redirect('perfil')
                except Exception as e:
                    return redirect('perfil')
        else:
            messages.error(request, ("Houve um erro ao iniciar o Script"))
            return redirect('perfil')
    else:
        return redirect('perfil')
