from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Vehicule, Log

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
    
    #template = loader.get_template("gmax_km/liste_vehicules.html")
    context = {"liste_vehicules": liste_vehicules}
    #return HttpResponse(template.render(context, request))
    return render(request, "gmax_km/liste_vehicules.html", context)
    

def detail_vehicules(request, vehicule_id):
    msg = f"detail vehicules {vehicule_id}"
    return HttpResponse(msg)

def ajouter_vehicules(request):
    msg = f"ajouter_vehicules"
    return HttpResponse(msg)

def modifier_vehicules(request,vehicule_id):
    msg = f"modifier vehicules {vehicule_id}"
    return HttpResponse(msg)

def supprimer_vehicules(request,vehicule_id):
    msg = f"supprimer vehicules {vehicule_id}"
    return HttpResponse(msg)
