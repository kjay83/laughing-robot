
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_employes, name="liste_employes_url"),
    path('ajouter/', views.ajouter_employes, name="ajouter_employes_url"),
    path('modifier/<int:id>', views.modifier_employes, name="modifier_employes_url"),
    path('supprimer/<int:id>', views.supprimer_employes, name="supprimer_employes_url"),
]