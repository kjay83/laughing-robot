from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import PlayerForm

# Create your views here.
def liste_players(request):
    liste_players = Player.objects.order_by("alias")    
    context = {"players": liste_players}
    return render(request, "aerial/player/liste_players.html", context)

def detail_players(request,player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = {"player": player}
    return render(request, "aerial/player/detail_players.html", context)

def creer_players(request):
    form = PlayerForm(request.POST or None)
    if form.is_valid() :
        form.save()
        return redirect('aerial:liste_players_url')
    return render(request, 'aerial/player/formulaire_players.html' , {'form' : form})

def modifier_players(request,player_id):
    player = get_object_or_404(Player,id=player_id)
    form = PlayerForm(request.POST or None, instance=player)
    if form.is_valid() :
        form.save()
        return redirect('aerial:detail_players_url',player_id=player.id)
    return render(request, 'aerial/player/formulaire_players.html' , {'form' : form})

def supprimer_players(request,player_id):
    player = get_object_or_404(Player,id=player_id)
    if request.method == "POST":
        player.delete()
        return redirect('aerial:liste_players_url')
    return render(request, 'aerial/player/confirmer_suppression_players.html' , {'player' : player})



def dashboard(request, identifier):
    try:
        # Essayer d'abord comme ID (entier)
        player_id = int(identifier)
        player = get_object_or_404(Player.objects.prefetch_related('entreprises'), pk=player_id)
    except ValueError:
        # Pas un ID, chercher par alias
        player = get_object_or_404(Player.objects.prefetch_related('entreprises'), alias=identifier)
    
    context = {"player": player}
    return render(request, "aerial/dashboard_player.html", context)

def detail_players(request,player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = {"player": player}
    return render(request, "aerial/player/detail_players.html", context)

def minijeu_mangue(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    minijeu, created = MiniJeuMangue.objects.get_or_create(player=player)
    context = {"player": player, "minijeu": minijeu}
    return render(request, "aerial/minijeu_mangue.html", context)

# Vue pour gérer les clics sur le manguier
def clic_mangue(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    minijeu, created = MiniJeuMangue.objects.get_or_create(player=player)
    context = {"player": player, "minijeu": minijeu}
    # On ajoute le cash_flow au cash actuel
    player.cash += minijeu.cash_flow
    player.save()
    
    # On renvoie juste le petit bout de texte (ou un template partiel)
    # avec le nouveau montant formaté
    return render(request, 'aerial/partials/minijeu_mangue/stat_cash_amount.html', {'player_cash': player.cash})