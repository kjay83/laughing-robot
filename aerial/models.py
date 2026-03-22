'''
NOTES POUR LES AVIONS:
- on simplifie la gestion des avions au maximum
- pas d'aeroport
- un avion ne peut etre affecté qu'a une seule ligne aerienne a la fois
- les trajets sont des strings composées des abbreviations des villes
- chaque joueur peut avoir plusieurs hubs
- une ligne aerienne ne peut avoir qu'un seul hub
- seuls quelques villes peuvent etre des hub
'''
from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
import math

class Pays(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="CG",max_length=50,unique=True)
    
    def __str__(self):
        return f"{self.abbreviation}"

class Ville(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="NON DEFINI",max_length=15,unique=True)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    peut_etre_hub = models.BooleanField(default=False,blank=True)
    prix_location_hub = models.DecimalField(default=0,max_digits=20,decimal_places=2,blank=True,null=True)
    demande = models.DecimalField(default=0.1,max_digits=3,decimal_places=2,blank=True,null=True)
    
    def __str__(self):
        return f"{self.abbreviation}"

class DistanceEntreDeuxVilles(models.Model):
    ville1 = models.ForeignKey(Ville, on_delete=models.CASCADE,related_name="dist_origine")
    ville2 = models.ForeignKey(Ville, on_delete=models.CASCADE,related_name="dist_destination")
    km = models.IntegerField(default=1,blank=True)

    def __str__(self):
        return f"{self.ville1}-{self.ville2}-{self.km}"

class Trajet(models.Model):
    nom = models.CharField(max_length=300,blank=True,null=True)
    km = models.IntegerField(default=1,blank=True)
    nb_escales = models.IntegerField(default=0,blank=True)
    depart = models.ForeignKey(Ville,on_delete=models.CASCADE,related_name="debut_trajet",blank=True,null=True)
    arrivee = models.ForeignKey(Ville,on_delete=models.CASCADE, related_name="fin_trajet",blank=True,null=True)
    #a partir d'une escale, sert pour faire le lien entre les trancons d'un trajet,
    etapes = models.ManyToManyField(DistanceEntreDeuxVilles,blank=True)
        
    def __str__(self):
        return f"{self.nom}"



class TypeBienImmobilier(models.TextChoices):
    APPARTEMENT = "APPART", "Appartement" 
    VILLA = "VILLA", "Villa"
    HOTEL = "HOTEL", "Hôtel"
    COMMERCE = "COMMERCE", "Commerce"
    BUREAUX = "BUREAUX", "Bureaux"
    ENTREPOT = "ENTREPOT", "Entrepôt"
    MANOIR = "MANOIR", "Manoir" 
    CHATEAU = "CHATEAU", "Château" 
 
class BienImmobilier(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True, unique=True)
    prix = models.DecimalField(default=0,max_digits=20, decimal_places=2,blank=True,null=True)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200,blank=True,null=True)
    cash_flow = models.DecimalField(default=0,max_digits=20, decimal_places=2,blank=True,null=True)
    lvl = models.IntegerField(default=1,blank=True,null=True)
    type_bien_immobilier = models.CharField(default=TypeBienImmobilier.VILLA, choices=TypeBienImmobilier, max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Player(models.Model):
    nom = models.CharField(max_length=200,blank=True,null=True)
    prenom = models.CharField(default='NON DEFINI',max_length=200,blank=True,null=True)
    alias = models.CharField(default='ALIAS',max_length=200,unique=True)
    email = models.EmailField(default='aucun@fail.com',max_length=200,blank=True,null=True)
    cash = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    biens_immobiliers = models.ManyToManyField(BienImmobilier, blank=True, related_name='proprietaires')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,editable=False)
    
    @property
    def total_cash_flow(self):
            """Cash flow généré/heure par toutes les entreprises"""
            total = self.entreprises.aggregate(
                total=models.Sum('cash_flow')
            )['total']
            return total if total is not None else 0

    def __str__(self):
        return f"{self.nom}"
    
    def initialize(self,starting_cash):
        self.cash = starting_cash
    
    def receive(self,amount):
        self.cash += amount
    
    def pay(self,amount):
        self.cash -= amount
    
    def clean(self):
        """Valider que l'alias ne peut pas être identique à un ID existant"""
        super().clean()
        
        # Essayer de convertir l'alias en entier
        try:
            alias_as_int = int(self.alias)
            # Vérifier si un Player avec cet ID existe (en excluant le joueur actuel lors de la modification)
            if Player.objects.filter(pk=alias_as_int).exclude(pk=self.pk).exists():
                raise ValidationError(
                    f"L'alias '{self.alias}' correspond à un ID existant. "
                    "Merci de choisir un autre alias."
                )
        except ValueError:
            # L'alias n'est pas un nombre, c'est OK
            pass
    
    def save(self, *args, **kwargs):
        """Valider avant de sauvegarder"""
        self.full_clean()
        super().save(*args, **kwargs)

class Entreprise(models.Model):    
    # Attributs communs à TOUTES les entreprises (ex: capital, niveau)
    class TypeEntreprise(models.TextChoices):
        COMPANIE_AERIENNE = "AER", "Companie Aerienne"
        BANQUE = "BQ", "Banque"
    type_entreprise =models.CharField(default=TypeEntreprise.COMPANIE_AERIENNE,
                                           choices=TypeEntreprise, max_length=5, blank=True, null=True)  
    nom = models.CharField(default="AIR AERIAL",max_length=200,
                           blank=True,null=True)
    abbreviation = models.CharField(default="AA",max_length=5,unique=True)
    proprietaire = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='entreprises')
    date_creation = models.DateTimeField(auto_now_add=True)
    niveau = models.IntegerField(default=1)
    cash_flow = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.abbreviation} ({self.proprietaire.alias})"
    
class CompagnieAerienne(Entreprise):
    def save(self, *args, **kwargs):
        # On force le type avant de sauvegarder si nouveau
        if not self.pk: # Si l'objet n'a pas encore d'ID, c'est une création
            self.type_entreprise = Entreprise.TypeEntreprise.COMPANIE_AERIENNE
        super().save(*args, **kwargs)

class Banque(Entreprise):
    def save(self, *args, **kwargs):
        # On force le type avant de sauvegarder si nouveau
        if not self.pk: # Si l'objet n'a pas encore d'ID, c'est une création
            self.type_entreprise = Entreprise.TypeEntreprise.BANQUE
        super().save(*args, **kwargs)
    

class Fabricant(models.Model):
    nom = models.CharField(max_length=100,blank=True,null=True)
    abbreviation = models.CharField(default="BOEING",max_length=10,unique=True)
    
    def __str__(self):
        return f"{self.abbreviation}"

class ModeleAvion(models.Model):
    nom = models.CharField(max_length=50)
    fabricant = models.ForeignKey(Fabricant, on_delete=models.SET_NULL,blank=True,null=True)
    nb_places = models.IntegerField(default=200,blank=True)
    nb_km_max_par_vol = models.IntegerField(default=3000,blank=True)
    nb_km_max_par_exploitation = models.IntegerField(default=10000,blank=True)
    nb_km_avant_maintenance = models.IntegerField(default=100,blank=True) 
    nb_heures_par_maintenance = models.DecimalField(default=1,max_digits=5, decimal_places=2,blank=True)
    maintenance_fee_percentage = models.DecimalField(default=10,max_digits=5, decimal_places=2,blank=True)
    prix_achat = models.DecimalField(default=100,max_digits=20, decimal_places=2,blank=True)

    def get_couts_maintenance(self) -> float:
        return self.prix_achat * self.maintenance_fee_percentage * self.nb_heures_maintenance
    
    def __str__(self):
        return f"{self.nom}"


class Avion(models.Model):
    class StatutAvion(models.TextChoices):
        EN_VOL = "VOL", "En vol"
        HANGAR = "HANGAR", "Hangar"
        MAINTENANCE = "MAINT" "Maintenance"
    compagnie = models.ForeignKey(CompagnieAerienne, on_delete=models.CASCADE,related_name='avions')
    # on utilise pas CASCADE pour le modele au cas ou on aurait des avions en vol/fonctionnement en cours
    modele = models.ForeignKey(ModeleAvion, on_delete=models.SET_NULL,null=True)
    est_a_maintenir = models.BooleanField(default=False,blank=True)
    est_amorti = models.BooleanField(default=False,blank=True)
    km_parcourus = models.IntegerField(default=0,blank=True)
    #TODO: faire des noms aleatoires
    nom_court = models.CharField(default="SILVARILLON",max_length=15,blank=True,null=True,unique=True)
    statut = models.CharField(default=StatutAvion.HANGAR,
                                      choices=StatutAvion,
                                      max_length=25, blank=True, null=True) 

    def verifier_amortissement(self) :
        if self.nb_heures_fonctionnement == self.modele.nb_km_max_par_exploitation :
            self.est_amorti = True
    
    def verifier_maintenance(self):
        if self.km_parcourus % self.modele.nb_km_maintenance == 0:
            self.est_a_maintenir = True
        
    def faire_maintenance(self):
        self.est_a_maintenir = False

    def __str__(self):
        return f"{self.compagnie.abbreviation}_{self.nom_court}"



#un hub est le QG d'ou partent tous les avions d'une companie
class Hub(models.Model):
    companie = models.ForeignKey(CompagnieAerienne, on_delete=models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.companie.abbreviation}_{self.ville}"

class LigneAerienne(models.Model):
    trajet = models.ForeignKey(Trajet,on_delete=models.CASCADE)
    hub = models.ForeignKey(Hub,on_delete=models.CASCADE)
    avions = models.ManyToManyField(Avion)
    
    def __str__(self):
        return f"{self.trajet}_{self.hub}"
    
class MiniJeuMangue(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    lvl = models.IntegerField(default=1,blank=True,null=True)
    #cash genere par click
    cash_flow = models.DecimalField(default=1.00,max_digits=20, decimal_places=2,blank=True,null=True)
    
    def get_coefficient_cash_flow(self, level: int) -> float:
    # Formule : 1.1 + (level * 0.1) + (level^2 / 100)
    # Au niveau 1 : ~1.2
    # Au niveau 10 : ~3.1
    # Au niveau 50 : ~31.1 (Le gain explose !)
        coefficient = round(1.1 + (level * 0.1) + (math.pow(level, 2) / 100), 2)
        return Decimal(str(coefficient))
    
    def get_coefficient_upgrade_cost(self, level: int) -> float:
    # Formule : Base * (1.5 ^ level)
    # Chaque niveau coûte 50% de plus que le précédent.
    # C'est ce qui rend le jeu "plus long" au fur et à mesure.
    # NB: Sile jeu devient trop dur trop vite, baisse le 1.5 du coût à 1.15 ou 1.2
        coefficient = round(math.pow(1.5, level), 2)
        return Decimal(str(coefficient))
    
    @property
    def get_level_up_cost(self) -> float:
        #autre methode : return 10 * (self.lvl ** 2)
        couts_de_base = 10.00
        couts_finaux = couts_de_base * float(self.get_coefficient_upgrade_cost(self.lvl))
        return Decimal(str(couts_finaux))
    
    @property
    def get_next_level_cash_flow(self) -> float:        
        next_level_cash_flow = float(self.cash_flow) * float(self.get_coefficient_cash_flow(self.lvl+1))
        return Decimal(str(next_level_cash_flow))
    
    def level_up(self):
        current_cost = self.get_level_up_cost
    
        if self.player.cash >= current_cost:
            self.player.cash -= current_cost

            # On applique le nouveau coefficient de gain
            self.cash_flow = self.get_next_level_cash_flow

            #on met a jour le lvl
            self.lvl += 1

            #sauvegarde des changements en bdd
            self.save()
            self.player.save()