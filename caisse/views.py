# caisse/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from commande.models import Commande
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Sum
from django.core.paginator import Paginator



@login_required
def recevoir_commandes(request):
    commandes = Commande.objects.filter(caissier_confirme=False)
    commandes_payees = Commande.objects.filter(caissier_confirme=True)

    total_montant_payes = commandes_payees.aggregate(total=Sum('montant_total'))['total'] or 0

    commandes_payees_details = []
    for commande in commandes_payees:
        details = []
        for commande_plat in commande.commandeplat_set.all():
            montant = commande_plat.plat.prix * commande_plat.quantite
            details.append({
                'plat_nom': commande_plat.plat.nom,
                'quantite': commande_plat.quantite,
                'prix_unitaire': commande_plat.plat.prix,
                'montant': montant
            })
        commandes_payees_details.append({
            'date_commande': commande.date_commande,
            'details': details
        })

    return render(request, 'caisse/commandes.html', {
        'commandes': commandes,
        'commandes_payees_details': commandes_payees_details,
        'total_montant_payes': total_montant_payes
    })

@login_required
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'caisse/detail_commande.html', {'commande': commande})

@login_required
def confirmer_paiement(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        commande.caissier_confirme = True
        commande.etat = 'Confirmée'
        commande.save()

        return redirect('recevoir_commandes')

    return render(request, 'caisse/detail_commande.html', {'commande': commande})
