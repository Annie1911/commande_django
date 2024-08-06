# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient, StockMovement
from .forms import IngredientForm
from django.utils import timezone
from django.db.models import F
from django.db import transaction

@login_required
def liste_ingredients(request):
    ingredients = Ingredient.objects.all()
    ingredients_faibles = [ingredient for ingredient in ingredients if ingredient.est_stock_faible()]
    return render(request, 'gestion/liste_ingredients.html', {
        'ingredients': ingredients,
        'ingredients_faibles': ingredients_faibles
    })

# Ajouter un ingrédient
@login_required
def ajouter_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            # Enregistrer le mouvement de stock
            StockMovement.objects.create(
                ingredient=ingredient,
                quantite=ingredient.quantite,
                mouvement_type='entrée',
                commentaire='Ajout initial de stock'
            )
            return redirect('liste_ingredients')
    else:
        form = IngredientForm()
    return render(request, 'gestion/ajouter_ingredient.html', {'form': form})

# Modifier un ingrédient
@login_required
def modifier_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    quantite_avant = ingredient.quantite  # Sauvegarder la quantité avant modification
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            ingredient = form.save()
            quantite_apres = ingredient.quantite  # Quantité après modification
            difference = quantite_apres - quantite_avant
            mouvement_type = 'entrée' if difference > 0 else 'sortie'
            # Enregistrer le mouvement de stock
            StockMovement.objects.create(
                ingredient=ingredient,
                quantite=abs(difference),
                mouvement_type=mouvement_type,
                commentaire=f'Modification de stock de {quantite_avant} à {quantite_apres}'
            )
            return redirect('liste_ingredients')
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'gestion/modifier_ingredient.html', {'form': form})

# Supprimer un ingrédient
@login_required
def supprimer_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        StockMovement.objects.create(
            ingredient=ingredient,
            quantite=ingredient.quantite,
            mouvement_type='sortie',
            commentaire='Suppression de l\'ingrédient'
        )
        ingredient.delete()
        return redirect('liste_ingredients')
    return render(request, 'gestion/supprimer_ingredient.html', {'ingredient': ingredient})

# Ajuster le stock d'un ingrédient
@login_required
def ajuster_stock(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    message = None
    if request.method == 'POST':
        quantite_sortie = request.POST.get('quantite_sortie')
        if quantite_sortie:
            quantite_sortie = float(quantite_sortie)
            if quantite_sortie <= 0:
                message = "La quantité à retirer doit être positive."
            elif quantite_sortie > ingredient.quantite:
                message = "La quantité à retirer ne peut pas être supérieure à la quantité en stock."
            else:
                quantite_avant = ingredient.quantite
                nouvelle_quantite = quantite_avant - quantite_sortie

                ingredient.quantite = nouvelle_quantite
                ingredient.save()
                StockMovement.objects.create(
                    ingredient=ingredient,
                    quantite=quantite_sortie,
                    mouvement_type='sortie',
                    commentaire=f'Ajustement de stock : retrait de {quantite_sortie} unités'
                )
                message = "Le stock a été ajusté avec succès."
                return redirect('liste_ingredients')
    return render(request, 'gestion/ajuster_stock.html', {'ingredient': ingredient, 'message': message})


# Historique des mouvements de stock
@login_required
def historique_mouvements_stock(request):
    mouvements = StockMovement.objects.all().order_by('-date_mouvement')
    return render(request, 'gestion/historique_mouvements_stock.html', {'mouvements': mouvements})
