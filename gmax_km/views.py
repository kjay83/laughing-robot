from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Vehicule, Log
from .forms import VehiculeForm

# LOGS
def index(request):
    liste_logs = Log.objects.order_by("-date_log")    
    context = {"logs": liste_logs}
    return render(request, "gmax_km/logs/liste_logs.html", context)

def detail_logs(request, log_id):
    log = get_object_or_404(Log,id=log_id)
    return render(request, 'gmax_km/logs/detail_logs.html' , {'log' : log})

def ajouter_logs(request):
    msg = f"ajouter_logs"
    return HttpResponse(msg)

def modifier_logs(request,log_id):
    msg = f"modifier log {log_id}"
    return HttpResponse(msg)

def supprimer_logs(request,log_id):
    msg = f"supprimer log {log_id}"
    return HttpResponse(msg)

# VEHICULES
def liste_vehicules(request):
    liste_vehicules = Vehicule.objects.order_by("immatriculation")    
    context = {"liste_vehicules": liste_vehicules}
    return render(request, "gmax_km/liste_vehicules.html", context)
    

def detail_vehicules(request, vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    return render(request, 'gmax_km/detail_vehicules.html' , {'vehic' : vehic})

def ajouter_vehicules(request):
    form = VehiculeForm(request.POST or None)
    if form.is_valid() :
        form.save()
        return redirect('gmax_km:liste_vehicules_url')
    return render(request, 'gmax_km/formulaire_vehicules.html' , {'form' : form})

def modifier_vehicules(request,vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    form = VehiculeForm(request.POST or None, instance=vehic)
    if form.is_valid() :
        form.save()
        return redirect('gmax_km:detail_vehicules_url',vehicule_id=vehic.id)
    return render(request, 'gmax_km/formulaire_vehicules.html' , {'form' : form})

def supprimer_vehicules(request,vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    if request.method == "POST":
        vehic.delete()
        return redirect('gmax_km:liste_vehicules_url')
    return render(request, 'gmax_km/confirmer_suppression_vehicules.html' , {'vehic' : vehic})
