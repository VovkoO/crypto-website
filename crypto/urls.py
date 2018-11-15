from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('prices/', views.prices, name="prices"),
    path('map/', views.map_site, name="map"),
    path('search/', views.search, name="search")
]