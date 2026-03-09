from django.contrib import admin

# Register your models here.
from .models import Vehicule, Log

admin.site.register(Vehicule)
admin.site.register(Log)