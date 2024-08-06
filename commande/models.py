from django.db import models
from django.conf import settings

class Categorie(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Plat(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='plats', null=True, blank=True)
    description = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='imgplat/',default=None,blank = True)

    def __str__(self):
        return self.nom

    def etat_disponibilite(self):
        return "Disponible" if self.disponible else "Non disponible"

class Commande(models.Model):
    ETAT_CHOICES = [
        ('En attente', 'En attente'),
        ('Confirmée', 'Confirmée'),
        ('Annulée', 'Annulée'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plats = models.ManyToManyField(Plat, through='CommandePlat')
    montant_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date_commande = models.DateTimeField(auto_now_add=True)
    caissier_confirme = models.BooleanField(default=False)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='En attente')
    motif_annulation = models.TextField(null=True, blank=True) 

    def __str__(self):
        return f"Commande {self.id} par {self.client.username}"

class CommandePlat(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=0)
    commentaire = models.TextField(blank=True, null=True)
    montant_plat_commande = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calculer le total à chaque sauvegarde
        self.montant_plat_commande = self.quantite * self.plat.prix
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite}x {self.plat.nom} pour Commande {self.commande.id}"
