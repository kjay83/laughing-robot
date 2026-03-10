from django.db import models

# Create your models here.
from datetime import datetime, date

from django.db import models
from django.utils import timezone

# Create your models here.
class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=200)
    marque = models.CharField(max_length=200)
    modele = models.CharField(default='AUCUN',max_length=200,blank=True)
    annee_fabrication = models.IntegerField(default=timezone.now().year,blank=True, null=True)
    date_acquisition = models.DateField(default=timezone.now(),blank=True, null=True)

    def __str__(self):
        return f"VEHICULE N° {self.id}|{self.immatriculation}|{self.marque}|{self.modele}|{self.annee_fabrication}|{self.date_acquisition}"
    

class Log(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    date_log = models.DateTimeField(default=timezone.now())
    km = models.IntegerField(default=0)

    def log_recent(self):
        return self.date_log >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return f"LOG N° {self.id}|{self.vehicule.immatriculation}|{self.date_log}|{self.km}"