from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['nom', 'quantite', 'unite_de_mesure', 'prix_unitaire', 'seuil_alerte']
