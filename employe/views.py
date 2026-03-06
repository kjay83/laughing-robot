from django.shortcuts import render
from .models import Employe

# Create your views here.

def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'employe/list.html' , {'employes' : employes})
