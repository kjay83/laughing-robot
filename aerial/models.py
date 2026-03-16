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

class CompagnieAerienne(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    nom = models.CharField(default="AIR AERIAL",max_length=200)
    cash = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    cash_flow = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    type_entreprise =models.CharField(default="COMPANIE_AERIENNE",max_length=200,blank=True,null=True)

    def __str__(self):
        return f"{self.nom}"

#TODO: faire heriter les types d'entreprise de la classe entreprise
# #class CompagnieAerienne(Entreprise):
    #def __init__(self):
       # self.type_entreprise="COMPANIE_AERIENNE"

   # def faire_voler_flotte(self):
    #    self.cash += 10

class modeleAvion(models.Model):
    nom = models.CharField(max_length=50)
    fabricant = models.CharField(max_length=50,blank=True,null=True)
    nb_places = models.IntegerField(default=200,blank=True)
    nb_km_max_par_vol = models.IntegerField(default=3000,blank=True)
    nb_km_max_par_exploitation = models.IntegerField(default=10000,blank=True)
    nb_km_maintenance = models.IntegerField(default=100,blank=True) 
    nb_heures_maintenance = models.DecimalField(default=1,max_digits=5, decimal_places=2,blank=True)
    maintenance_fee_percentage = models.IntegerField(default=10,blank=True)
    prix_achat = models.DecimalField(default=100,max_digits=20, decimal_places=2)

    def get_couts_maintenance(self) -> float:
        return self.prix_achat * self.maintenance_fee_percentage * self.nb_heures_maintenance
    
    def __str__(self):
        return f"{self.fabricant}_{self.nom}"


class Avion(models.Model):
    compagnie = models.ForeignKey(CompagnieAerienne, on_delete=models.CASCADE)
    modele = models.ForeignKey(modeleAvion, on_delete=models.CASCADE)
    nb_heures_fonctionnement = models.DecimalField(default=0,max_digits=5, decimal_places=2,blank=True)
    est_a_maintenir = models.BooleanField(default=False,blank=True)
    est_amorti = models.BooleanField(default=False,blank=True)
    km_parcourus = models.IntegerField(default=0,blank=True)
    #numero de l'avion dans la flotte
    indicatif_flotte = models.IntegerField(default=0,blank=True)

    def verifie_amortissement(self) :
        if self.nb_heures_fonctionnement == self.modele.nb_km_max_par_exploitation :
            self.est_amorti = True
    
    def verifie_maintenance(self):
        if self.km_parcourus % self.modele.nb_km_maintenance == 0:
            self.est_a_maintenir = True
        
    def faire_maintenance(self):
        self.est_a_maintenir = False

    def __str__(self):
        return f"{self.compagnie}_{self.modele}_{self.indicatif}"

