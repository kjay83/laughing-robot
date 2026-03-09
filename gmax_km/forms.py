from django import forms
from .models import Vehicule

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ["immatriculation","marque","modele","annee_fabrication","annee_acquisition"]
        widgets = {
            'immatriculation' : forms.TextInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'immatriculation',
            }),
            'marque' : forms.TextInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'marque',
            }),
            'modele' : forms.TextInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'modele',
            }),
            'annee_fabrication' : forms.DateField(attrs= {
                'class' : 'input w-full',
                'placeholder': 'annee_fabrication"',
            }),
            'annee_acquisition' : forms.DateField(attrs= {
                'class' : 'input w-full',
                'placeholder': 'annee_acquisition"',
            })
        }