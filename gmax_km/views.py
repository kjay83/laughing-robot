from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Vehicule, Log
from .forms import VehiculeForm, LogForm

# LOGS----------------------------------------------------
def index(request):
    liste_logs = Log.objects.order_by("-date_log")    
    context = {"logs": liste_logs}
    return render(request, "gmax_km/logs/liste_logs.html", context)

def index_tableau_logs(request):
    tableau_logs = Log.objects.order_by("-date_log")    
    context = {"logs": tableau_logs}
    return render(request, "gmax_km/logs/tableau_logs.html", context)

def detail_logs(request, log_id):
    log = get_object_or_404(Log,id=log_id)
    return render(request, 'gmax_km/logs/detail_logs.html' , {'log' : log})

#fonction pour sauvegarder le formulaire relatif aux logs de km
# C'est necessaire pour verifier si l'utilisateur existe
# et ne pas avoir une erreur avec la base si c'est null
def save_form_log(request, form):
    log_instance = form.save(commit=False)
        
    # On n'enregistre l'utilisateur QUE s'il est connecté
    if request.user.is_authenticated:
        log_instance.updated_by = request.user
    else:
        log_instance.updated_by = None  # Il reste vide
                   
    log_instance.save()

def ajouter_logs(request):
    form = LogForm(request.POST or None)
    if form.is_valid() :
        save_form_log(request, form)
        return redirect('gmax_km:liste_logs_url')
    return render(request, 'gmax_km/logs/formulaire_logs.html' , {'form' : form})

def modifier_logs(request,log_id):
    log = get_object_or_404(Log,id=log_id)
    form = LogForm(request.POST or None, instance=log)
    if form.is_valid() :
        save_form_log(request, form)
        return redirect('gmax_km:detail_logs_url',log_id=log.id)
    return render(request, 'gmax_km/logs/formulaire_logs.html' , {'form' : form})

def supprimer_logs(request,log_id):
    log = get_object_or_404(Log,id=log_id)
    if request.method == "POST":
        log.delete()
        return redirect('gmax_km:liste_logs_url')
    return render(request, 'gmax_km/logs/confirmer_suppression_logs.html' , {'log' : log})

# VEHICULES----------------------------------------------
def liste_vehicules(request):
    liste_vehicules = Vehicule.objects.order_by("immatriculation")    
    context = {"liste_vehicules": liste_vehicules}
    return render(request, "gmax_km/vehicules/liste_vehicules.html", context)
    

def detail_vehicules(request, vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    return render(request, 'gmax_km/vehicules/detail_vehicules.html' , {'vehic' : vehic})

def ajouter_vehicules(request):
    form = VehiculeForm(request.POST or None)
    if form.is_valid() :
        form.save()
        return redirect('gmax_km:liste_vehicules_url')
    return render(request, 'gmax_km/vehicules/formulaire_vehicules.html' , {'form' : form})

def modifier_vehicules(request,vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    form = VehiculeForm(request.POST or None, instance=vehic)
    if form.is_valid() :
        form.save()
        return redirect('gmax_km:detail_vehicules_url',vehicule_id=vehic.id)
    return render(request, 'gmax_km/vehicules/formulaire_vehicules.html' , {'form' : form})

def supprimer_vehicules(request,vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    if request.method == "POST":
        vehic.delete()
        return redirect('gmax_km:liste_vehicules_url')
    return render(request, 'gmax_km/vehicules/confirmer_suppression_vehicules.html' , {'vehic' : vehic})
