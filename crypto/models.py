from datetime import datetime

from django.db import models


class Orders(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(default=datetime.now)
    price = models.IntegerField(default=5000)
    quantity = models.IntegerField(default=1)


class Topic(models.Model):
    id_razdel = models.IntegerField(default=0)
    name_theme = models.CharField(max_length=200)
    name_creator = models.CharField(max_length=50)
    name_last_answer = models.CharField(max_length=200)
    date_last_answer = models.DateField(default=datetime.now)


class Message(models.Model):
    id_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    text_mes = models.CharField(max_length=300)
    name_man = models.CharField(max_length=50)
    date_answer = models.DateField(default=datetime.now)


