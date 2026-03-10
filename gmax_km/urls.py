from django.contrib import admin
from django.urls import path
from . import views

app_name= "gmax_km"
urlpatterns = [
    #LOGS URLS
    path("",views.index,name="liste_logs_url"),
    path('<int:log_id>', views.detail_logs, name="detail_logs_url"),
    path('ajouter/', views.ajouter_logs, name="ajouter_logs_url"),
    path('<int:log_id>/modifier', views.modifier_logs, name="modifier_logs_url"),
    path('<int:log_id>/supprimer', views.supprimer_logs, name="supprimer_logs_url"),
    #VEHICULES URLS
    path('vehicules/', views.liste_vehicules, name="liste_vehicules_url"),
    path('vehicules/<int:vehicule_id>', views.detail_vehicules, name="detail_vehicules_url"),
    path('vehicules/ajouter/', views.ajouter_vehicules, name="ajouter_vehicules_url"),
    path('vehicules/<int:vehicule_id>/modifier', views.modifier_vehicules, name="modifier_vehicules_url"),
    path('vehicules/<int:vehicule_id>/supprimer', views.supprimer_vehicules, name="supprimer_vehicules_url"),
]