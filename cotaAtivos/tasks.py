from .models import Acao, Preco, Perfil
from yahoo_fin.stock_info import get_quote_table
from background_task import background
from django.core.mail import send_mail

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
            l = Perfil.objects.all()
            for limite in l:
                lSup = getattr(limite, "limSup")
                lInf = getattr(limite, "limInf")
                if preco >= lSup:
                    manda_email("sup", str(acao), lSup, preco)
                if preco <= lInf:
                    manda_email("inf", str(acao), lInf, preco)
        except Exception as e:
            #print("Error")
            pass


def manda_email(limite, nome, valor, preco):
    e = Perfil.objects.all()
    for email in e:
        mail_to = getattr(email, "email")
        if limite == "sup":
            send_mail(
            'Venda a sua acao ' + nome,
            'Sua ação ' + nome + ' ultrapassou o limite estabelecido de venda de: ' + valor + '. No momento desse email ela vale: ' + preco,
            '',
            [mail_to],
            fail_silently=False,
            )
        if limite == "inf":
            send_mail(
            'Compre acao ' + nome,
            'A acao ' + nome + 'ultrapassou o limite estabelecido de compra de: ' + valor + '. No momento desse email ela vale: ' + preco,
            '',
            [mail_to],
            fail_silently=False,
            )