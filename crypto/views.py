from django.http import HttpResponse
from django.shortcuts import render
import json
import requests


def home(request):
    # Получение цен
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,XLM,LTC,USDT,XMR,DASH&tsyms=USD")
    price = json.loads(price_request.content)

    # Получуние Новостей
    api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api = json.loads(api_request.content)
    return render(request, 'home.html', {'api': api, 'price': price})


def prices(request):
    #Получение цен
    all_prices_request = requests.get("https://api.coinmarketcap.com/v2/ticker/")
    all_prices = json.loads(all_prices_request.content)
    return render(request, 'prices.html', {'all_prices': all_prices})


def map_site(request):
    return render(request, 'map.html', {})


def search(request):
    if request.method == 'POST':
        import requests
        import json
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote + "&tsyms=USD")
        crypto = json.loads(crypto_request.content)
        i = 1
        return render(request, 'search.html', {'quote':quote, 'crypto':crypto}, i)
    else:
        return render(request, 'search.html', {})

