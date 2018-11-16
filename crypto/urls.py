from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('prices/', views.prices, name="prices"),
    path('map/', views.map_site, name="map"),
    path('dynamic/', views.dynamic, name="dynamic"),
    path('moving/', views.moving, name="moving"),
    path('backcall/', views.backcall, name="backcall"),
    path('search/', views.search, name="search")
]