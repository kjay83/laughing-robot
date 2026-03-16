from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Player)
admin.site.register(Entreprise)
admin.site.register(CompagnieAerienne)
admin.site.register(modeleAvion)
admin.site.register(Avion)
