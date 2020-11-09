import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Location(models.Model):
    addressZH = models.CharField(max_length=200)
    nameZH = models.CharField(max_length=200)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    nameEN = models.CharField(max_length=200)
    addressEN = models.CharField(max_length=200)

    def __str__(self):
        return self.addressZH
