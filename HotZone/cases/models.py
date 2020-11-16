from django.db import models
from locations.models import Location


# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=50)
    hkid = models.CharField(max_length=20, default='---')
    birthday = models.DateField()

    def __str__(self):
        return self.hkid


class Virus(models.Model):
    name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=200)
    max_inf_period = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Case(models.Model):
    no = models.IntegerField(default=0)
    date_confirmed = models.DateField()
    local = models.CharField(max_length=10, choices=[('1', 'local'), ('2', 'imported')], default='local')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    virus = models.ForeignKey(Virus, on_delete=models.CASCADE)

    def __str__(self):
        return self.no


class CaseLocation(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    category = models.CharField(max_length=50, choices=[('1', 'Residence'), ('2', 'Workplace'), ('3', 'Visit')],
                                default='Residence')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
