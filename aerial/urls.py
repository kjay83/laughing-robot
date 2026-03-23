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
    
    #test d'url generique pour le dashboard qui accepte soit l'id soit l'alias du joueur
    #path('dashboard/<str:identifier>', views.dashboard_by_str, name="dashboard_url_by_str"),

    #page de depart pour les joueurs ,elle affiche des statistiques et des liens vers les minijeux
    path('joueur/<int:player_id>/dashboard', views.dashboard_by_id, name="dashboard_url_by_id"), 

    #pages pour le minijeu de la mangue
    path('joueur/<int:player_id>/mangue', views.minijeu_mangue, name="minijeu_mangue_url"),
    path('joueur/<int:player_id>/mangue/cash_up', views.clic_mangue_cash_up, name="clic_mangue_cash_up_url"), 
    path('joueur/<int:player_id>/mangue/level_up', views.clic_mangue_level_up, name="clic_mangue_level_up_url"),

    #pages pour le minijeu de l'aviation
    path('joueur/<int:player_id>/aviation', views.dashboard_aviation, name="dashboard_aviation_url"), 
    path('joueur/<int:player_id>/aviation/avion/acheter', views.acheter_avion, name="acheter_avion_url"), 
    path('joueur/<int:player_id>/aviation/avion/<int:avion_id>/gerer', views.gerer_avion, name="gerer_avion_url"), 
    path('joueur/<int:player_id>/aviation/avion/<int:avion_id>/vendre', views.vendre_avion, name="vendre_avion_url"), 
]