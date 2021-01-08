from .models import Acao, Preco, Email, Perfil
from yahoo_fin.stock_info import get_quote_table
from background_task import background
from django.core.mail import send_mail
from desafioInoa.settings import EMAIL_HOST_USER

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
            limite = Perfil.objects.get(pk=acao.id)
            #print(getattr(limite, "limInf"))
            lSup = float(getattr(limite, "limSup"))
            lInf = float(getattr(limite, "limInf"))
            print(str(lInf) + ' \ ' + str(lSup))
            if float(preco["Quote Price"]) >= float(lSup):
                manda_email("sup", str(acao), lSup, preco["Quote Price"])
            if float(preco["Quote Price"]) <= float(lInf):
                manda_email("inf", str(acao), lInf, preco["Quote Price"])
        except Exception as e:
            print("Error")
            pass


def manda_email(limite, nome, valor, preco):
    e = Email.objects.all()
    for email in e:
        mail_to = getattr(email, "email")
        if limite == "sup":
            assunto = 'Venda a sua acao [{}]'.format(nome.upper())
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
            assunto = 'Compre acao [{}]'.format(nome.upper())
            msg = 'A ação {} ultrapassou o limite estabelecido de compra de: {:.2f}. No momento desse email ela vale: {:.2f}'.format(nome.upper(), valor, preco)
            send_mail(
            assunto,
            msg,
            EMAIL_HOST_USER,
            [mail_to],
            fail_silently=False
            )
            print("mandei email inferior")