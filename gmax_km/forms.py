from django import forms
from .models import Vehicule, Log

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ["immatriculation","marque","modele","annee_fabrication","date_acquisition"]
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
            'annee_fabrication' : forms.NumberInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'annee_fabrication"',
            }),
            'date_acquisition' : forms.DateInput(
                format='%Y-%m-%d',
                attrs= {
                'class' : 'input w-full',
                'type': 'date',
                }
            )
        }

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ["date_log","vehicule","km"]
        widgets = {
            'date_log' : forms.DateInput(
                format='%Y-%m-%d',
                attrs= {
                'class' : 'input w-full',
                'type': 'date',
                }
            ),
            'vehicule' : forms.Select(attrs= {
                'class' : 'input w-full',
                'placeholder': 'immatriculation',
            }),
            'km' : forms.NumberInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'kilometrage"',
            }),
        }