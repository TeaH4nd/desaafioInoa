from django.shortcuts import render
import yfinance as yf


def home(request):
    import requests
    import json 

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
