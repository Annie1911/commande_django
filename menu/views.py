from django.shortcuts import render, redirect, get_object_or_404
from commande.models import Plat, Categorie, Commande
from django.contrib import messages
from commande.forms import CategorieForm, PlatForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@login_required
def commandes_reçu(request):
    commandes = Commande.objects.filter(caissier_confirme=False).order_by('-date_commande')
    return render(request, 'menu/commandes_reçu.html', {'commandes': commandes})

@login_required
def gerer_menu(request):
    plats = Plat.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'menu/gerer_menu.html', {'plats': plats, 'categories': categories})

@login_required
def ajouter_plat(request):
    if request.method == 'POST':
        form = PlatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerer_menu')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = PlatForm()
    return render(request, 'menu/ajouter_plat.html', {'form': form})

@login_required
def modifier_plat(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)
    if request.method == 'POST':
        form = PlatForm(request.POST, instance=plat)
        if form.is_valid():
            form.save()
            return redirect('gerer_menu')
    else:
        form = PlatForm(instance=plat)
    return render(request, 'menu/modifier_plat.html', {'form': form})

@login_required
def supprimer_plat(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)
    plat.delete()
    return redirect('gerer_menu')

@login_required
def gerer_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'menu/gerer_categories.html', {'categories': categories})

@login_required
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerer_categories')
    else:
        form = CategorieForm()
    return render(request, 'menu/ajouter_categorie.html', {'form': form})

@login_required
def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('gerer_categories')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'menu/modifier_categorie.html', {'form': form})

@login_required
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    categorie.delete()
    return redirect('gerer_categories')

@login_required
def delete_all_plats_in_category(request, category_id):
    categorie = get_object_or_404(Categorie, id=category_id)
    categorie.plats.all().delete()
    return redirect('gerer_menu')

@login_required
def annuler_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    if request.method == 'POST':
        motif = request.POST.get('motif')
        commande.etat = 'Annulée'
        commande.caissier_confirme = False
        commande.motif_annulation = motif
        commande.save()

        # Logique de notification
        channel_layer = get_channel_layer()

        notification_message = {
            'type': 'commande_message',
            'message': f"Commande n°{commande.id} annulée. Motif : {motif} par le responsable"
        }

        # Notifier le client
        async_to_sync(channel_layer.group_send)(
            f'client_{commande.client.id}',
            notification_message
        )

        # Notifier le caissier
        async_to_sync(channel_layer.group_send)(
            'caissiers',
            notification_message
        )

        return redirect('commandes_reçu')
    
    return render(request, 'menu/annuler_commande.html', {'commande': commande})
