# commande/forms.py

from django import forms
from .models import Plat, Categorie

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['name']


class PlatForm(forms.ModelForm):
    class Meta:
        model = Plat
        fields = ['nom', 'prix', 'disponible', 'categorie','description', 'image']



class DeleteAllPlatsForm(forms.Form):
    confirmation = forms.BooleanField(label='Confirmer la suppression de tous les plats', required=True)