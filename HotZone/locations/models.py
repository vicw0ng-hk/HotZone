from django.db import models


# Create your models here.
class Location(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
