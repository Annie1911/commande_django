# gestion/models.py

from django.db import models
from django.utils import timezone

class Ingredient(models.Model):
    nom = models.CharField(max_length=100)
    quantite = models.FloatField()
    unite_de_mesure = models.CharField(max_length=50, blank=True, null=True)
    prix_unitaire = models.FloatField()
    seuil_alerte = models.FloatField(default=10)

    def __str__(self):
        return self.nom

    def calculer_prix_total(self):
        return self.quantite * self.prix_unitaire

    def est_stock_faible(self):
        return self.quantite <= self.seuil_alerte

class StockMovement(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    date_mouvement = models.DateTimeField(default=timezone.now)
    quantite = models.FloatField()
    mouvement_type = models.CharField(max_length=10, choices=[('entrée', 'Entrée'), ('sortie', 'Sortie')])
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.mouvement_type} de {self.quantite} {self.ingredient.unite_de_mesure} de {self.ingredient.nom}"
