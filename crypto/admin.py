from django.contrib import admin
from .models import Orders, Topic, Message


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'date', 'price', 'quantity')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'id_razdel', 'name_theme', 'name_creator', 'name_last_answer', 'date_last_answer')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'id_topic', 'text_mes', 'name_man', 'date_answer')


admin.site.register(Orders, OrdersAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Message, MessageAdmin)