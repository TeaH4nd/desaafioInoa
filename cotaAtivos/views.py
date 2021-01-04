from django.shortcuts import render

def home(request):
    import requests
    import json 

    if request.method == 'POST':
        simbolo = request.POST['simbolo']

        api_request = requests.get("https://api.hgbrasil.com/finance/stock_price?key=a5508924&symbol={}".format(simbolo))

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = 200

        apiList = list(api['results'].values())
        return render(request, 'home.html', {'api':apiList[0]})
    else:
        return render(request, 'home.html', {'simbolo':"Digite um simbolo acima para pesquisa"})
