from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Vehicule, Log
from .forms import VehiculeForm

# LOGS
def index(request):
    msg = f"liste logs acuueils."
    return HttpResponse(msg)

def detail_logs(request, log_id):
    msg = f"detail logs {log_id}"
    return HttpResponse(msg)

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
    liste_vehicules = Vehicule.objects.order_by("-immatriculation")    
    context = {"liste_vehicules": liste_vehicules}
    return render(request, "gmax_km/liste_vehicules.html", context)
    

def detail_vehicules(request, vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    return render(request, 'gmax_km/detail_vehicules.html' , {'vehic' : vehic})

def ajouter_vehicules(request):
    msg = f"ajouter_vehicules"
    return HttpResponse(msg)

def modifier_vehicules(request,vehicule_id):
    vehic = get_object_or_404(Vehicule,id=vehicule_id)
    form = VehiculeForm(request.POST or None, instance=vehic)
    if form.is_valid() :
        form.save()
        return redirect('gmax_km:liste_vehicules_url')
    return render(request, 'gmax_km/formulaire_vehicule.html' , {'form' : form})

def supprimer_vehicules(request,vehicule_id):
    msg = f"supprimer vehicules {vehicule_id}"
    return HttpResponse(msg)
