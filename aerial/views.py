from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import PlayerForm
from django.core.paginator import Paginator

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



def dashboard_by_str(request, identifier):
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


def dashboard_by_id(request, player_id):    
    player = get_object_or_404(Player.objects.prefetch_related('entreprises'), pk=player_id)
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
    
    avions = Avion.objects.prefetch_related('compagnie').filter(compagnie__proprietaire__pk = player.pk).order_by("compagnie__abbreviation","nom_court") 
    for a in avions:
        print(f"dans liste avions : ID=:{a.id} - {a}")
    print(f"Avions for player in avions = {avions.count()}")
    #context = {"player": player, "compagnies_aeriennes": compagnies_aeriennes, "avions": avions}

    #on recupere le mot cle de recherche
    query = request.GET.get('q', '')    
    # On récupère le nombre de pages choisi, sinon 10 par défaut
    par_page = request.GET.get('per_page', 10)
    
    # Filtrage : on cherche dans l'immatriculation du véhicule lié
    tableau = Avion.objects.prefetch_related('compagnie').filter(compagnie__proprietaire__pk = player.pk).order_by("compagnie__abbreviation","nom_court")
    if query:
        tableau = avions.filter(nom_court__icontains=query)
    
    # On définit 10 logs par page
    paginator = Paginator(tableau, par_page) 
    
    # On récupère le numéro de la page dans l'URL (ex: ?page=2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "avions": page_obj, 
        'par_page': int(par_page),
        'query': query,
        'player': player
    }

    #context = {"player": player, "compagnies_aeriennes": compagnies_aeriennes, "avions": avions}
    return render(request, "aerial/aviation/dashboard_aviation.html", context)


def acheter_avion(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = {"player": player}
    return HttpResponse(f"AVION ACHAT: contexte is = to {context}")
    #return render(request, "aerial/aviation/acheter_avion.html", context)


def gerer_avion(request, player_id, avion_id):
    player = get_object_or_404(Player, pk=player_id)
    avion = get_object_or_404(Avion, pk=avion_id)
    context = {"player": player, "avion": avion}
    return HttpResponse(f"AVION GERER: contexte is = to {context}")
    #return render(request, "aerial/aviation/acheter_avion.html", context)

def vendre_avion(request, player_id,avion_id):
    player = get_object_or_404(Player, pk=player_id)
    avion = get_object_or_404(Avion, pk=avion_id)
    context = {"player": player, "avion": avion}
    return HttpResponse(f"AVION VENDRE: contexte is = to {context}")
    #return render(request, "aerial/aviation/acheter_avion.html", context)