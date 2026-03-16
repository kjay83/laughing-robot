from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Player)
#admin.site.register(Entreprise)
admin.site.register(CompagnieAerienne)
admin.site.register(modeleAvion)
admin.site.register(Avion)
admin.site.register(Continent)
admin.site.register(Pays)
admin.site.register(Ville)
admin.site.register(Aeroport)
admin.site.register(DistanceEntreDeuxVilles)
admin.site.register(FlotteCompanieAerienne)
admin.site.register(HubCompanieAerienne)
admin.site.register(LignesParHub)
admin.site.register(AvionParFlotte)
