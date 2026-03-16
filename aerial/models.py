from django.db import models

class Player(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(default='AUCUN',max_length=200,blank=True)
    alias = models.CharField(default='AUCUN',max_length=200,blank=True)
    email = models.EmailField(default='aucun@fail.com',max_length=200,blank=True)
    money = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom}"
    
    def initialize(self,starting_money):
        self.money = starting_money
    
    def receive(self,amount):
        self.money += amount
    
    def pay(self,amount):
        self.money -= amount

class Entreprise(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    nom = models.CharField(default="ENTREPRISE",max_length=200)
    cash = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    cash_flow = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    type_entreprise =models.CharField(default="CLASSIQUE",max_length=200,blank=True,null=True)

class CompagnieAerienne(Entreprise):
    def __init__(self):
        self.type_entreprise="COMPANIE_AERIENNE"

    def faire_voler_flotte(self):
        self.cash += 10

class modeleAvion(models.Model):
    nom = models.CharField(max_length=50)
    nb_places = models.IntegerField(default=200,blank=True)
    nb_heures_max = models.FloatField(default=48,blank=True)
    nb_heures_maintenance = models.FloatField(default=1,blank=True)
    maintenance_fee_percentage = models.IntegerField(default=10,blank=True)
    prix_achat = models.DecimalField(default=100,max_digits=20, decimal_places=2)

    def get_couts_maintenance(self) -> float:
        return self.prix_achat * self.maintenance_fee_percentage * self.nb_heures_maintenance


class Avion(models.Model):
    compagnie = models.ForeignKey(CompagnieAerienne, on_delete=models.CASCADE)
    modele = models.ForeignKey(modeleAvion, on_delete=models.CASCADE)



