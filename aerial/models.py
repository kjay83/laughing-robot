from django.db import models

class Pays(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="CG",max_length=50,unique=True)
    
    def __str__(self):
        return f"{self.abbreviation}"

class Ville(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="PNR",max_length=10)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.abbreviation}"

class DistanceEntreDeuxVilles(models.Model):
    ville1 = models.ForeignKey(Ville, on_delete=models.CASCADE,related_name="depart")
    ville2 = models.ForeignKey(Ville, on_delete=models.CASCADE,related_name="arrivee")
    km = models.IntegerField(default=1,blank=True)

    def __str__(self):
        return f"{self.ville1}-{self.ville2}-{self.km}"
    
class Player(models.Model):
    nom = models.CharField(max_length=200,blank=True,null=True)
    prenom = models.CharField(default='NON DEFINI',max_length=200,blank=True,null=True)
    alias = models.CharField(default='ALIAS',max_length=200,unique=True)
    email = models.EmailField(default='aucun@fail.com',max_length=200,blank=True,null=True)
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
    class TypeEntreprise(models.TextChoices):
        COMPANIE_AERIENNE = "AER", "Companie Aerienne"
        BANQUE = "BQ", "Banque"
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    nom = models.CharField(default="AIR AERIAL",max_length=200,blank=True,null=True)
    abbreviation = models.CharField(default="AA",max_length=5,unique=True)
    cash = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    cash_flow = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    type_entreprise =models.CharField(default=TypeEntreprise.COMPANIE_AERIENNE,
                                      choices=TypeEntreprise,
                                      max_length=25, blank=True, null=True)    

    def __str__(self):
        return f"{self.abbreviation}"

class Fabricant(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="BOEING",max_length=10,unique=True)
    
    def __str__(self):
        return f"{self.abbreviation}"

class modeleAvion(models.Model):
    nom = models.CharField(max_length=50)
    fabricant = models.ForeignKey(Fabricant, on_delete=models.SET_NULL)
    nb_places = models.IntegerField(default=200,blank=True)
    nb_km_max_par_vol = models.IntegerField(default=3000,blank=True)
    nb_km_max_par_exploitation = models.IntegerField(default=10000,blank=True)
    nb_km_avant_maintenance = models.IntegerField(default=100,blank=True) 
    nb_heures_par_maintenance = models.DecimalField(default=1,max_digits=5, decimal_places=2,blank=True)
    maintenance_fee_percentage = models.DecimalField(default=10,max_digits=3, decimal_places=2,blank=True)
    prix_achat = models.DecimalField(default=100,max_digits=20, decimal_places=2,blank=True)

    def get_couts_maintenance(self) -> float:
        return self.prix_achat * self.maintenance_fee_percentage * self.nb_heures_maintenance
    
    def __str__(self):
        return f"{self.fabricant}_{self.nom}"


class Avion(models.Model):
    compagnie = models.ForeignKey(CompagnieAerienne, on_delete=models.CASCADE)
    modele = models.ForeignKey(modeleAvion, on_delete=models.SET_NULL)
    est_a_maintenir = models.BooleanField(default=False,blank=True)
    est_amorti = models.BooleanField(default=False,blank=True)
    km_parcourus = models.IntegerField(default=0,blank=True)
    nom_court = models.CharField(default="SILVARILLON",max_length=15,blank=True,null=True)

    def verifier_amortissement(self) :
        if self.nb_heures_fonctionnement == self.modele.nb_km_max_par_exploitation :
            self.est_amorti = True
    
    def verifier_maintenance(self):
        if self.km_parcourus % self.modele.nb_km_maintenance == 0:
            self.est_a_maintenir = True
        
    def faire_maintenance(self):
        self.est_a_maintenir = False

    def __str__(self):
        return f"{self.compagnie}_{self.modele}_{self.indicatif_flotte}"



#liste tous les hubs du jeu
class HubCompanieAerienne(models.Model):
    #TODO: verifier que le nom est unique dans la table
    nom = models.CharField(default="HUB",max_length=50,blank=True,null=True)
    companie = models.ForeignKey(CompagnieAerienne, on_delete=models.CASCADE)
    aeroport = models.ForeignKey(Aeroport, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.aeroport}_{self.id}"

#lien entre flotte et hub
#dans un hub donne j'ai quelles flottes?
class FlotteCompanieAerienne(models.Model):
    nom = models.CharField(default="FLOTTE",max_length=50,blank=True,null=True)
    hub = models.ForeignKey(HubCompanieAerienne, on_delete=models.SET_NULL,blank=True,null=True)
    #avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nom}_{self.hub}"
    
class LignesParHub(models.Model):
    hub = models.ForeignKey(HubCompanieAerienne, on_delete=models.CASCADE)
    trajet = models.ForeignKey(DistanceEntreDeuxVilles, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.trajet}_{self.hub.id}"

#lien entre avion et flotte
#dans une flotte donne j'ai quels avions?
class AvionParFlotte(models.Model):
    flotte = models.ForeignKey(FlotteCompanieAerienne, on_delete=models.CASCADE)
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.flotte}_{self.avion.indicatif_flotte}"

#Affectations des avions sur les lignes
#dans une ligne donne quels sont les avions qui y volent
class AvionParLignes(models.Model):
    ligne = models.ForeignKey(LignesParHub, on_delete=models.CASCADE)
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.ligne}_{self.avion.indicatif_flotte}"
