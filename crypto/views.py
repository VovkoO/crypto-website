from django.shortcuts import render, redirect, render_to_response
import json
import requests
from .models import Orders, Topic, Message
from django.contrib import auth
from django.core.mail import send_mail
import datetime

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
        order = all_orders.get(pk=request.POST.get('order_id'))
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


def forum(request):
    username = auth.get_user(request).get_username()
    user_permission = auth.get_user(request).is_staff
    topics = Topic.objects.all()
    if request.POST:
        if 'message' in request.POST:
            new_message = Message.objects.create()
            new_message.date_answer = datetime.datetime.now()
            new_message.name_man = username
            new_message.text_mes = request.POST.get('message')
            new_topic = Topic.objects.create()
            new_topic.name_theme = request.POST.get('topic')
            new_topic.name_creator = username
            new_topic.date_last_answer = new_message.date_answer
            new_topic.name_last_answer = new_message.name_man
            new_topic.save()
            new_message.id_topic = new_topic
            new_message.save()
        else:
            Topic.objects.get(pk=request.POST.get('topic_id')).delete()
    return render(request, 'forum.html', {'user': username, 'permission': user_permission, 'topics': topics})


def change_topic_name(request):
    if 'topic_name' in request.POST:
        topic = Topic.objects.get(pk=int(request.POST.get('topic_id')))
        topic.name_theme = request.POST.get('topic_name')
        topic.save()
        return redirect('forum')
    topic_id = request.POST.get('topic_id')
    return render(request, 'change_topic_name.html', {'user': auth.get_user(request).get_username(), 'topic_id': topic_id})


def topic(request):
    username = auth.get_user(request).get_username()
    user_permission = auth.get_user(request).is_staff
    if request.POST:
        if 'message_id' in request.POST:
            Message.objects.get(pk=request.POST.get('message_id')).delete()
        elif 'message' in request.POST:
            topic = Topic.objects.get(pk=request.POST.get('topic_id'))
            new_message = Message.objects.create()
            new_message.id_topic = topic
            new_message.name_man = username
            new_message.date_answer = datetime.datetime.now()
            new_message.text_mes = request.POST.get('message')
            new_message.save()
            topic.name_last_answer = username
            topic.date_last_answer = new_message.date_answer
            topic.save()
        topic_id = request.POST.get("topic_id")
        messages = Message.objects.filter(id_topic=Topic.objects.get(pk=topic_id)).order_by('-pk')
        return render(request, 'topic.html', {'user': username, 'messages': messages, 'topic_id': topic_id, 'user_permission': user_permission})
    return redirect('forum')


def add_topic(request):
    username = auth.get_user(request).get_username()
    return render(request, 'add_topic.html', {'user': username})


def add_message(request):
    username = auth.get_user(request).get_username()
    if request.POST:
        topic_id = request.POST.get('topic_id')
        return render(request, 'add_message.html', {'user': username, 'topic_id': topic_id})
    return redirect('forum')
