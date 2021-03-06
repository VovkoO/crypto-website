from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('prices/', views.prices, name="prices"),
    path('map/', views.map_site, name="map"),
    path('dynamic/', views.dynamic, name="dynamic"),
    path('moving/', views.moving, name="moving"),
    path('backcall/', views.backcall, name="backcall"),
    path('bigsearch/', views.bigsearch, name="bigsearch"),
    path('orders/', views.orders, name="orders"),
    path('edit_order/', views.edit_order, name="edit_order"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('search_order/', views.search_order, name="search_order"),
    path('send_email/', views.send_email, name="send_email"),
    path('forum/', views.forum, name="forum"),
    path('change_topic_name/', views.change_topic_name, name="change_topic_name"),
    path('topic/', views.topic, name="topic"),
    path('add_topic/', views.add_topic, name="add_topic"),
    path('add_message/', views.add_message, name="add_message"),
    path('search/', views.search, name="search")
]