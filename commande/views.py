from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Plat, Commande, CommandePlat, Categorie
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def consulter_menu(request):
    categories = Categorie.objects.all()
    return render(request, 'commande/menu.html', {'categories': categories})

@login_required
def index(request):
    return render(request, 'commande/index.html')

@login_required
def ajouter_au_panier(request):
    if request.method == 'POST':
        # Trouver toutes les commandes non confirmées pour l'utilisateur
        commandes = Commande.objects.filter(client=request.user, caissier_confirme=False)
        
        if commandes.exists():
            # On suppose qu'il y a une seule commande active pour l'utilisateur
            commande = commandes.first()
        else:
            # Créer une nouvelle commande s'il n'y en a pas
            commande = Commande.objects.create(client=request.user, caissier_confirme=False)
        
        for plat_id in request.POST.getlist('plat_id'):
            plat = Plat.objects.get(id=plat_id)
            quantite = int(request.POST.get(f'quantite_{plat_id}', 1))
            commentaire = request.POST.get(f'commentaire_{plat_id}', '')

            commande_plat, created = CommandePlat.objects.get_or_create(commande=commande, plat=plat)
            commande_plat.quantite += quantite
            commande_plat.commentaire = commentaire
            commande_plat.save()

            commande.montant_total += plat.prix * quantite
            commande.save()

    return redirect('consulter_panier')

@login_required
def consulter_panier(request):
    try:
        commande = Commande.objects.get(client=request.user, caissier_confirme=False)
        commande_plats = commande.commandeplat_set.all()

        for commande_plat in commande_plats:
            commande_plat.montant_plat_commande = commande_plat.plat.prix * commande_plat.quantite

        total = sum(commande_plat.montant_plat_commande for commande_plat in commande_plats)

        return render(request, 'commande/panier.html', {'commande': commande, 'commande_plats': commande_plats, 'total': total})
    except Commande.DoesNotExist:
        return redirect('consulter_menu')

@login_required
def confirmer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        # commande.caissier_confirme = True  # Ne pas changer ce champ ici
        commande.save()

        # Notify via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'commandes',
            {
                'type': 'commande_message',
                'message': {
                    'id': commande.id,
                    'client': commande.client.username,
                    'montant_total': commande.montant_total,
                    'plats': [
                        {
                            'nom': cp.plat.nom,
                            'quantite': cp.quantite,
                            'commentaire': cp.commentaire if cp.commentaire else ""
                        } for cp in commande.commandeplat_set.all()
                    ]
                }
            }
        )
        return redirect('confirmation', commande_id=commande.id)

@login_required
def modifier_commande(request, commande_plat_id):
    commande_plat = get_object_or_404(CommandePlat, id=commande_plat_id)
    if request.method == 'POST':
        quantite = request.POST.get('quantite')
        commentaire = request.POST.get('commentaire')
        commande_plat.quantite = quantite
        commande_plat.commentaire = commentaire
        commande_plat.save()
        return redirect('consulter_panier')  # Redirige vers la vue du panier
    return redirect('consulter_panier')  # Redirige vers la vue du panier si la méthode n'est pas POST

@login_required
def confirmation(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande/confirmation.html', {'commande': commande})

@login_required
def commande_annuler(request, commande_id):
    try:
        commande = Commande.objects.get(id=commande_id, client=request.user, caissier_confirme=False)
        commande.delete()
    except Commande.DoesNotExist:
        pass
    return redirect('consulter_menu')
