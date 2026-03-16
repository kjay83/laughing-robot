from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["nom","prenom","alias","email"]
        widgets = {
            'nom' : forms.TextInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'nom',
            }),
            'prenom' : forms.TextInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'prenom',
            }),
            'alias' : forms.TextInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'alias',
            }),
            'email' : forms.EmailInput(attrs= {
                'class' : 'input w-full',
                'placeholder': 'email',
            }),
        }
