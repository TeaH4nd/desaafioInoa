from django.core.mail import send_mail
from desafioInoa.settings import EMAIL_HOST_USER

from .models import Acao, Preco, Email, Perfil, Salvo

import yfinance as yf
from yahoo_fin.stock_info import get_quote_table
from background_task import background


@background(schedule=5)
def get_precos():
    acoes = Acao.objects.all()
    for acao in acoes:
        try:
            print(str(acao))
            preco = get_quote_table(str(acao))
            #print(preco)
            p = acao.preco_set.create(preco = preco["Quote Price"])
            p.save()
            #print("limites")
            try:
                limite = Perfil.objects.get(pk=acao.id)
            except Perfil.DoesNotExist:
                limite = False
            #print(getattr(limite, "limInf"))
            if limite:
                lSup = float(getattr(limite, "limSup"))
                lInf = float(getattr(limite, "limInf"))
                print(str(lInf) + ' \ ' + str(lSup))
                if float(preco["Quote Price"]) >= float(lSup):
                    manda_email("sup", str(acao), lSup, preco["Quote Price"])
                if float(preco["Quote Price"]) <= float(lInf):
                    manda_email("inf", str(acao), lInf, preco["Quote Price"])
            else:
                print("Limite de {} não adicionado".format(str(acao)))
        except Exception as e:
            print("Error")
            pass
    atualizar()


def manda_email(limite, nome, valor, preco):
    e = Email.objects.all()
    for email in e:
        mail_to = getattr(email, "email")
        if limite == "sup":
            assunto = 'Venda a sua ação [{}]'.format(nome.upper())
            msg = 'Sua ação {} ultrapassou o limite estabelecido de venda de: {:.2f}. No momento desse email ela vale: {:.2f}'.format(nome.upper(), valor, preco)
            send_mail(
            assunto,
            msg,
            EMAIL_HOST_USER,
            [mail_to],
            fail_silently=False
            )
            print("mandei email superior")

        if limite == "inf":
            assunto = 'Compre ação [{}]'.format(nome.upper())
            msg = 'A ação {} ultrapassou o limite estabelecido de compra de: {:.2f}. No momento desse email ela vale: {:.2f}'.format(nome.upper(), valor, preco)
            send_mail(
            assunto,
            msg,
            EMAIL_HOST_USER,
            [mail_to],
            fail_silently=False
            )
            print("mandei email inferior")

def atualizar():
    simbolo = Acao.objects.all()
    acoes = []
    for item in simbolo:
        #print(item.id)
        try:
            api_request = yf.Ticker(str(item))
            api_request.info["id"] = item.id
            acoes.append(api_request.info)
        except Exception as e:
            print("erro atualizando")
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