from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from desafioInoa.settings import EMAIL_HOST_USER

from .forms import AcaoForm, EmailForm, TempoForm, LimiteForm
from .models import Acao, Preco, Salvo, Email, Perfil, TaskTime
from .tasks import get_precos, atualizar

import yfinance as yf
from yahoo_fin.stock_info import get_quote_table
from background_task.models import CompletedTask, Task

# view para renderizar a ação pesquisada
def home(request):
    if request.method == 'POST':
        simbolo = request.POST['simbolo']
        simbolo = simbolo + ".sa"
        #print(simbolo)
        try:
            api_request = yf.Ticker(str(simbolo))
            return render(request, 'home.html', {'api':api_request.info})
            #print(api_request)
        except Exception as e:
            messages.error(request, 'Simbolo não encontrado!')
            return redirect('home.html')

        #apiList = list(api['results'].values())
    else:
        return render(request, 'home.html', {'error':"Digite um simbolo acima para pesquisar"})

# view para renderizar a tabela com as info de todas as ações adicionadas pelo usuario
#   nela tem o form de adicionar novas ações no modelo Acao para futuras consultas
def portifolio(request):
    if request.method == 'POST':
        form = AcaoForm(request.POST or None)
        if form.is_valid():
            try:
                simbolo = form.cleaned_data['simbolo'] + ".sa"
                #print(simbolo)
                api_request = yf.Ticker(simbolo)
                print(api_request.info['symbol'])
            except Exception as e:
                api_request = 500

            if (api_request != 500):
                try:
                    acao = form.save(commit=False)
                    acao.simbolo = simbolo
                    acao.save()
                    atualizar()
                    messages.success(request, ("Adicionado com Sucesso!"))
                    return redirect('portifolio')
                except Exception as e:
                    messages.warning(request, ("Erro ao adicionar a ação!"))
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
            dictAcoes["symbol"] = getattr(item, "simbolo")[:-3]
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

# função para deletar a ação do modelo Acao e Salvo, excluindo-a do banco de dados
def delete(request, acao_id):
    itemA = Acao.objects.get(pk=acao_id)
    itemS = Salvo.objects.get(pk=acao_id)
    itemA.delete()
    itemS.delete()
    messages.success(request, ("Deletado com Sucesso!"))
    return redirect('portifolio')

# função para deletar o email do modelo Email, excluindo-a do banco de dados
def deleteEmail(request, email_id):
    email = Email.objects.get(pk=email_id)
    email.delete()
    messages.success(request, ("Deletado com Sucesso!"))
    return redirect('perfil')

# view para renderizar todos os preços salvos de uma certa ação
#   nela tem o form de criar ou atualizar os limites da ação
def acao(request, acao_id):
    if request.method == 'POST':
        req = request.POST.copy()
        req["limSup"] = request.POST["limSup"].replace(",",".")
        req["limInf"] = request.POST["limInf"].replace(",",".")
        form = LimiteForm(req or None)
        #print(form)
        if (form.is_valid()):
            print("form is valid")
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

# view para renderizar os dados salvos que o usuário adicionou
#   nela tem o form de adicionar novos emails no modelo Email
#   tem o form de adicionar o periodo de repetição do get_precos()
#   tem uma tabela mostrando todos os limites de cada ação
def perfil(request):
    if request.method == 'POST':
        if "email" in request.POST:
            form = EmailForm(request.POST or None)
            if (form.is_valid()):
                form.save()
                messages.success(request, ("Adicionado com Sucesso!"))
                return redirect('perfil')
            else:
                messages.warning(request, ("Houve um erro ao adicionar o email. O email ja esta adicionado?"))
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
            limite["simbolo"] = str(getattr(item, "simbolo")).upper()[:-3]
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

# view para iniciar o script get_precos() dado um certo periodo de repeticao
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
            messages.success(request, ("Script inicializado com sucesso!"))
            task.save()
        else:
            messages.error(request, ("Houve um erro ao iniciar o Script"))
            return redirect('perfil')
    else:
        return redirect('perfil')

#view para parar o script get_precos()
def stop_get_precos(request):
    Task.objects.all().delete()
    TaskTime.objects.all().delete()
    return redirect('perfil')