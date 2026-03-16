from django.db import models




class Continent(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="ABBR",max_length=50)
    
    def __str__(self):
        return f"{self.abbreviation}"

class Pays(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="ABBR",max_length=50)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.abbreviation}"

class Ville(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="ABBR",max_length=50)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.abbreviation}"

class Aeroport(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="ABBR",max_length=50)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.ville}_{self.abbreviation}"

class DistanceEntreDeuxVilles(models.Model):
    ville1 = models.ForeignKey(Ville, on_delete=models.CASCADE,related_name="ville1rel")
    ville2 = models.ForeignKey(Ville, on_delete=models.CASCADE,related_name="ville2rel")
    km = models.IntegerField(default=1,blank=True)

    def __str__(self):
        return f"{self.ville1}-{self.ville2}-{self.km}"
    
class Player(models.Model):
    nom = models.CharField(max_length=200,blank=True,null=True)
    prenom = models.CharField(default='AUCUN',max_length=200,blank=True,null=True)
    #TODO: s'assurer que UNIQUE dans la BDD
    alias = models.CharField(default='AUCUN',max_length=200,unique=True)
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
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    #TODO: verifier que le nom est unique dans la table
    nom = models.CharField(default="AIR AERIAL",max_length=200,blank=True,null=True)
    abbreviation = models.CharField(default="AA",max_length=5,unique=True)
    cash = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    cash_flow = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    type_entreprise =models.CharField(default="COMPANIE_AERIENNE",max_length=200,blank=True,null=True)
    

    def __str__(self):
        return f"{self.abbreviation}"

#TODO: faire heriter les types d'entreprise de la classe entreprise
# #class CompagnieAerienne(Entreprise):
    #def __init__(self):
       # self.type_entreprise="COMPANIE_AERIENNE"

   # def faire_voler_flotte(self):
    #    self.cash += 10

class modeleAvion(models.Model):
    nom = models.CharField(max_length=50)
    #TODO: transformer en ENUM
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
    #TODO: s'assurer qu'il est unique dans la flotte
    indicatif_flotte = models.IntegerField(default=1,blank=True)
    nom_court = models.CharField(default="FE",max_length=10,blank=True,null=True)

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
