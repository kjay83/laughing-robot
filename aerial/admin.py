from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Player)
admin.site.register(CompagnieAerienne)
admin.site.register(modeleAvion)
admin.site.register(Avion)
admin.site.register(Pays)
admin.site.register(Ville)
admin.site.register(DistanceEntreDeuxVilles)
admin.site.register(Trajet)
admin.site.register(Hub)
admin.site.register(LigneAerienne)
admin.site.register(Fabricant)
