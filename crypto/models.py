from datetime import datetime

from django.db import models


class Orders(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(default=datetime.now)
    price = models.IntegerField(default=5000)
    quantity = models.IntegerField(default=1)
