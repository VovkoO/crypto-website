from django.db import models


class Orders(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    price = models.FloatField()
    quantity = models.IntegerField()
