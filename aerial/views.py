from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Player
from .forms import PlayerForm

# Create your views here.
def liste_players(request):
    liste_players = Player.objects.order_by("-created_at")    
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