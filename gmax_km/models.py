from django.db import models

# Create your models here.
from datetime import datetime, date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def get_current_year():
    return timezone.now().year

# Create your models here.
class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=200)
    marque = models.CharField(max_length=200)
    modele = models.CharField(default='AUCUN',max_length=200,blank=True)
    annee_fabrication = models.IntegerField(default=get_current_year,blank=True, null=True)
    date_acquisition = models.DateField(default=timezone.now,blank=True, null=True)

    def __str__(self):
        return f"{self.immatriculation}"
    

class Log(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    date_log = models.DateTimeField(default=timezone.now)
    km = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, editable=False)

    def log_recent(self):
        return self.date_log >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return f"{self.id}|{self.vehicule.immatriculation}|{self.date_log}"