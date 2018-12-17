from django.contrib import admin
from .models import Orders



class OrdersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'date', 'price', 'quantity')


admin.site.register(Orders, OrdersAdmin)