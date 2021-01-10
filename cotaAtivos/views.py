from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import AcaoForm, EmailForm, TempoForm, LimiteForm
from .models import Acao, Preco, Salvo, Email, Perfil, TaskTime
from .tasks import get_precos

import yfinance as yf
from yahoo_fin.stock_info import get_quote_table
from background_task.models import CompletedTask, Task

from django.core.mail import send_mail
from desafioInoa.settings import EMAIL_HOST_USER

import datetime, time

def index(request):
    return render(request, 'index.html', {})

def home(request):
    import requests
    #import json 

    if request.method == 'POST':
        simbolo = request.POST['simbolo']
        simbolo = simbolo + ".sa"
        #print(simbolo)
        #api_request = requests.get("https://api.hgbrasil.com/finance/stock_price?key=a5508924&symbol={}".format(simbolo))
        try:
            api_request = yf.Ticker(str(simbolo))
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
        if form.is_valid():
            try:
                simbolo = form.cleaned_data['simbolo'] + ".sa"
                #print(simbolo)
                api_request = yf.Ticker(simbolo)
            except Exception as e:
                api_request = 500

            if (api_request != 500):
                acao = form.save(commit=False)
                acao.simbolo = simbolo
                acao.save()
                messages.success(request, ("Adicionado com Sucesso!"))
                atualizar(request)
                return redirect('portifolio')
            else:
                messages.error(request, ("Ação não encontrada."))
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
    itemA = Acao.objects.get(pk=acao_id)
    itemS = Salvo.objects.get(pk=acao_id)
    itemA.delete()
    itemS.delete()
    messages.success(request, ("Deletado com Sucesso!"))
    return redirect('portifolio')

def deleteEmail(request, email_id):
    email = Email.objects.get(pk=email_id)
    email.delete()
    messages.success(request, ("Deletado com Sucesso!"))
    return redirect('perfil')


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
    if request.method == 'POST':
        form = LimiteForm(request.POST or None)
        #print(form)
        if (form.is_valid()):
            try:
                p = Perfil.objects.get(pk=acao_id)
                print(p)
                l = form.save(commit=False)
                p.limSup = l.limSup
                p.limInf = l.limInf
                p.save()
                messages.success(request, ("Limites atualizados com Sucesso!"))
                return redirect('acao', acao_id)
            except Exception as e:
                acao = Acao.objects.get(pk=acao_id)
                print(acao)
                l = form.save(commit=False)
                acao.perfil_set.create(id = acao_id, limSup = l.limSup, limInf = l.limInf)
                messages.success(request, ("Limites criados com Sucesso!"))
                return redirect('acao', acao_id)
        else:
            messages.error(request, ("Houve um erro ao adicionar os limites."))
            return redirect('acao', acao_id)
    else:
        precos = Preco.objects.filter(simbolo=acao_id).order_by('-data')
        acao = Salvo.objects.get(pk=acao_id)
        try:
            limites = Perfil.objects.get(pk=acao_id)
            lim = {}
            lim["limInf"] = getattr(limites, "limInf")
            lim["limSup"] = getattr(limites, "limSup")
        except Exception as e:
            lim = {}
        nome = getattr(acao, "nome")
        listPrecos = []
        for preco in precos:
            dictPreco = {}
            dictPreco["preco"] = getattr(preco, "preco")
            dictPreco["data"] = getattr(preco, "data")
            listPrecos.append(dictPreco)
        return render(request, 'acao.html', {'lista':listPrecos, "acao":nome, "acao_id":acao_id, "limites":lim})

def perfil(request):
    if request.method == 'POST':
        if "email" in request.POST:
            form = EmailForm(request.POST or None)
            if (form.is_valid()):
                form.save()
                messages.success(request, ("Adicionado com Sucesso!"))
                return redirect('perfil')
            else:
                messages.error(request, ("Houve um erro ao adicionar o email. O email ja esta adicionado?"))
                return redirect('perfil')
                   
    else:
        p = Perfil.objects.all()
        e = Email.objects.all()
        emailList = []
        for item in e:
            email = {}
            email["id"] = getattr(item, "id")
            email["email"] = getattr(item, "email")
            emailList.append(email)
        limites = []
        for item in p:
            limite = {}
            limite["simbolo"] = getattr(item, "simbolo")
            limite["limInf"] = getattr(item, "limInf")
            limite["limSup"] = getattr(item, "limSup")
            limites.append(limite)
        task = TaskTime.objects.all()
        if task:
            for item in task:
                taskDict = {}
                taskDict['numero'] = getattr(item, "numero")
                taskDict['tempo'] = getattr(item, "tempo")
            return render(request, 'perfil.html', {"lista":emailList, "task":taskDict, "limite":limites})
        return render(request, 'perfil.html', {"lista":emailList, "task":False, "limite":limites})

def start_get_precos(request):
    if request.method == 'POST':
        form = TempoForm(request.POST or None)
        if (form.is_valid()):
            numero = form.cleaned_data['numero']
            tempo = form.cleaned_data['tempo']
            task = TaskTime()
            task.numero = numero
            if tempo == 1:
                try:
                    CompletedTask.objects.all().delete()
                    Task.objects.all().delete()
                    get_precos(repeat= (numero))
                    task.tempo = "segundo(s)"
                    task.save()
                    return redirect('perfil')
                except Exception as e:
                    return redirect('perfil')
            elif tempo == 2:
                try:
                    CompletedTask.objects.all().delete()
                    Task.objects.all().delete()
                    get_precos(repeat= (numero*60))
                    task.tempo = "minuto(s)"
                    task.save()
                    return redirect('perfil')
                except Exception as e:
                    return redirect('perfil')
            elif tempo == 3:
                try:
                    CompletedTask.objects.all().delete()
                    Task.objects.all().delete()
                    get_precos(repeat= (numero*60*60))
                    task.tempo = "hora(s)"
                    task.save()
                    return redirect('perfil')
                except Exception as e:
                    return redirect('perfil')
            task.save()

        else:
            messages.error(request, ("Houve um erro ao iniciar o Script"))
            return redirect('perfil')
    else:
        return redirect('perfil')

def stop_get_precos(request):
    Task.objects.all().delete()
    TaskTime.objects.all().delete()
    return redirect('perfil')