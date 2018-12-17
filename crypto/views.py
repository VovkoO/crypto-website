from django.shortcuts import render, redirect, render_to_response
import json
import requests
from .models import Orders
from django.contrib import auth
from django.core.mail import send_mail

from django.contrib.auth.forms import UserCreationForm


def home(request):
    # Получение цен
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,XLM,LTC,USDT,XMR,DASH&tsyms=USD")
    price = json.loads(price_request.content)

    # Получуние Новостей
    api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api = json.loads(api_request.content)
    # if user is not None:
    #     return render(request, 'home.html', {'api': api, 'price': price, 'user': user})
    return render(request, 'home.html', {'api': api, 'price': price, 'user': auth.get_user(request).get_username()})


def prices(request):
    #Получение цен
    all_prices_request = requests.get("https://api.coinmarketcap.com/v2/ticker/")
    all_prices = json.loads(all_prices_request.content)
    return render(request, 'prices.html', {'all_prices': all_prices, 'user': auth.get_user(request).get_username()})


def map_site(request):
    return render(request, 'map.html', {'user': auth.get_user(request).get_username()})


def orders(request):
    all_orders = Orders.objects.all()
    if request.method == 'POST':
        order = all_orders.get(pk=request.POST['order_id'])
        order.delete()
    return render(request, 'orders.html', {'all_orders': all_orders, 'user': auth.get_user(request).get_username()})


def bigsearch(request):
    return render(request, 'bigsearch.html', {'user': auth.get_user(request).get_username()})


def edit_order(request):
    all_orders = Orders.objects.all()

    if request.method == 'POST' and 'change_order' in request.POST:
        order = all_orders.get(pk=request.POST['order_id'])
        order.name = request.POST.get('order_name')
        if order.date != "":
            order.date = request.POST.get('date')
        order.price = request.POST.get('price')
        order.quantity = request.POST.get('quantity')

        order.save()
        return render(request, 'edit_order.html', {'order': order, 'user': auth.get_user(request).get_username()})

    elif request.method == 'POST':
        order = all_orders.get(pk=request.POST['order_id'])
        return render(request, 'edit_order.html', {'order': order, 'user': auth.get_user(request).get_username()})

    return render(request, 'edit_order.html', {'user': auth.get_user(request).get_username()})


def moving(request):
    return render(request, 'moving.html', {})


def backcall(request):
    return render(request, 'backcall.html', {'user': auth.get_user(request).get_username()})


def dynamic(request):
    price_request = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,LTC,NEO&tsyms=USD")
    price = json.loads(price_request.content)
    BTC_price = price['RAW']['BTC']['USD']['PRICE']
    ETH_price = price['RAW']['ETH']['USD']['PRICE']
    LTC_price = price['RAW']['LTC']['USD']['PRICE']
    NEO_price = price['RAW']['NEO']['USD']['PRICE']
    return render(request, 'dynamic.html', {'BTC': BTC_price, 'ETH': ETH_price, 'LTC': LTC_price, 'NEO': NEO_price, 'user': auth.get_user(request).get_username()})


def search(request):
    if request.method == 'POST':
        import requests
        import json
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote + "&tsyms=USD")
        crypto = json.loads(crypto_request.content)
        i = 1
        return render(request, 'search.html', {'quote':quote, 'crypto':crypto, 'user': auth.get_user(request).get_username()}, i)
    else:
        return render(request, 'search.html', {'user': auth.get_user(request).get_username()})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Пользователь не найден', 'user': auth.get_user(request).get_username()})
    return render(request, 'login.html', {'user': auth.get_user(request).get_username()})


def logout(request):
    auth.logout(request)
    return redirect('home')


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            redirect('home')
        else:
            form = newuser_form
    return render(request, 'register.html', {'form': form, 'user': auth.get_user(request).get_username()})


def search_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Orders.objects.filter(name=name):
            orders = Orders.objects.filter(name=request.POST.get('name'))
            return render(request, 'search_order.html', {'orders': orders, 'user': auth.get_user(request).get_username()})
        else:
            return render(request, 'search_order.html', {'user': auth.get_user(request).get_username(), 'error': 'Пользователей не найдено'})
    return render(request, 'search_order.html', {'user': auth.get_user(request).get_username()})


def send_email(request):
    if request.POST:
        message = request.POST.get('message')
        email = request.POST.get('email')
        send_mail('crypto_news', message, 'cryptonews659@gmail.com', [email], fail_silently=False)
        return render(request, 'send_email.html', {'user': auth.get_user(request).get_username(), 'result': 'Сообщение отправлено'})
    return render(request, 'send_email.html', {'user': auth.get_user(request).get_username()})