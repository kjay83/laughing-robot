from django.contrib import admin
from django.urls import path
from . import views

app_name= "aerial"
urlpatterns = [
    #PLAYER URLS
    path("",views.liste_players,name="liste_players_url"),
    path("player/",views.liste_players,name="liste_players_url"),
    path("player/<int:player_id>",views.detail_players,name="detail_players_url"),
    path('player/creer/', views.creer_players, name="creer_players_url"),
    path('player/<int:player_id>/modifier', views.modifier_players, name="modifier_players_url"),
    path('player/<int:player_id>/supprimer', views.supprimer_players, name="supprimer_players_url"),
    #page de depart pour les joueurs ,elle affiche des statistiques et des liens vers les minijeux
    path('dashboard/<str:identifier>', views.dashboard, name="dashboard_url"),
    path('joueur/<int:player_id>/mangue', views.minijeu_mangue, name="minijeu_mangue_url"),
    path('joueur/<int:player_id>/mangue/clic', views.clic_mangue, name="clic_mangue_url"), 
]