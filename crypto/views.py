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


def bigsearch(request):
    return render(request, 'bigsearch.html', {})


def moving(request):
    return render(request, 'moving.html', {})


def backcall(request):
    return render(request, 'backcall.html', {})


def dynamic(request):
    price_request = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,LTC,NEO&tsyms=USD")
    price = json.loads(price_request.content)
    BTC_price = price['RAW']['BTC']['USD']['PRICE']
    ETH_price = price['RAW']['ETH']['USD']['PRICE']
    LTC_price = price['RAW']['LTC']['USD']['PRICE']
    NEO_price = price['RAW']['NEO']['USD']['PRICE']
    return render(request, 'dynamic.html', {'BTC': BTC_price, 'ETH': ETH_price, 'LTC': LTC_price, 'NEO': NEO_price})


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

