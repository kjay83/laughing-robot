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
    """
    Affiche le dashboard d'un joueur.
    
    Le dashboard est accessible par son ID (entier) ou par son alias.
    Il affiche les statistiques globales du joueur, ainsi que des liens vers ses minijeux.
    
    Parameters:
        request (HttpRequest): La requête HTTP
        identifier (str): L'ID ou l'alias du joueur

    Returns:
        HttpResponse: La page HTML du dashboard
    """
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

# Vue pour gérer les clics sur le manguier (cash up)
def clic_mangue_cash_up(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    minijeu, created = MiniJeuMangue.objects.get_or_create(player=player)
    # On ajoute le cash_flow au cash actuel
    player.cash += minijeu.cash_flow
    player.save()
    
    # On renvoie juste le petit bout de texte (ou un template partiel)
    # avec le nouveau montant formaté
    player.refresh_from_db()  # Assure que player a les données les plus récentes de la base de données
    context = {'player_cash': player.cash}
    return render(request, 'aerial/partials/minijeu_mangue/stat_cash_amount.html', context )

# Vue pour gérer les clics sur le bouton levelup du manguier (lv up)
def clic_mangue_level_up(request, player_id):
    # SUPPRESSION De cette ligne pour eviter les soucis de 
    # désynchronisation d'instances d'objets en mémoire (ou "Object Identity" dans l'ORM).
    #on utilise une seule source de verite au lieu d'avoir 2 variables pointant vers le même enregistrement en #bdd mais qui ne sont pas synchronisées (player et minijeu.player)
    # #player = get_object_or_404(Player, pk=player_id)
    minijeu, created = MiniJeuMangue.objects.get_or_create(player=get_object_or_404(Player, pk=player_id))
    print(f"Player cash before level up: {minijeu.player.cash}")
    print(f"Level before level up: {minijeu.lvl}")
    minijeu.level_up()
    
    # On renvoie juste le petit bout de texte (ou un template partiel)
    # avec le nouveau montant formaté
    print(f"Player cash after level up: {minijeu.player.cash}")
    print(f"Level ater level up: {minijeu.lvl}")
    context = {'player_cash': minijeu.player.cash,
                'minijeu_level': minijeu.lvl,
                'minijeu_cash_flow': minijeu.cash_flow,
                'minijeu_level_up_cost': minijeu.get_level_up_cost,
                'minijeu_next_level_cash_flow': minijeu.get_next_level_cash_flow}
    return render(request, 'aerial/partials/minijeu_mangue/stat_level_cash_flow_amount.html', context )
    
def dashboard_aviation(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    compagnies_aeriennes = CompagnieAerienne.objects.prefetch_related('avions').filter(proprietaire__pk=player.pk)
    #print(f"Player {player.id} is {player.alias} and has {player.cash} cash")
    #print(f"Companies aeriennes for player {player.id}: {compagnies_aeriennes.count()}")
    #for c in compagnies_aeriennes:
        #print(f"dans liste compagnies aeriennes : ID=:{c.id} - {c} - ({c.avions.count()} avions)")
        #for a in c.avions.all():
            #print(f"--- avion N° {a.id} : - {a}")
    
    #avions = Avion.objects.prefetch_related('compagnie').filter(compagnie__proprietaire__pk = player.pk)
    #for a in avions:
    #    print(f"dans liste avions : ID=:{a.id} - {a}")
    #print(f"Avions for player in avions = {avions.count()}")
    #context = {"player": player, "compagnies_aeriennes": compagnies_aeriennes, "avions": avions}
    context = {"player": player, "compagnies_aeriennes": compagnies_aeriennes}
    return render(request, "aerial/aviation/dashboard_aviation.html", context)