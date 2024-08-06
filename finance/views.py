from django.shortcuts import render
from commande.models import Commande, Plat, CommandePlat
from .forms import DateRangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, FloatField
from django.utils.timezone import now, make_aware
from datetime import datetime, time
from django.db import DatabaseError
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader

@login_required
def consulter_ventes(request):
    form = DateRangeForm(request.GET or None)
    ventes_totales = 0
    repartition_par_plat = []
    plats_populaires = []
    variations_ventes = []
    revenus_par_categorie = []

    date_unique = None
    error_message = None

    if form.is_valid():
        try:
            period_choice = form.cleaned_data['period_choice']
            if period_choice == 'today':
                date_unique = now().date()
                date_debut = make_aware(datetime.combine(date_unique, time.min))
                date_fin = make_aware(datetime.combine(date_unique, time.max))
            else:
                date_unique = form.cleaned_data.get('date')
                if date_unique:
                    date_debut = make_aware(datetime.combine(date_unique, time.min))
                    date_fin = make_aware(datetime.combine(date_unique, time.max))
                else:
                    date_debut = make_aware(datetime.combine(now().date(), time.min))
                    date_fin = make_aware(datetime.combine(now().date(), time.max))

            # Debugging: Print dates to console
            print(f"Date Début: {date_debut}")
            print(f"Date Fin: {date_fin}")

            commandes = Commande.objects.filter(
                caissier_confirme=True,
                etat='Confirmée',
                date_commande__range=[date_debut, date_fin]
            )

            # Debugging: Print commandes to console
            print(f"Commandes trouvées: {commandes}")

            # Calcul des ventes totales
            ventes_totales = commandes.aggregate(total=Sum('montant_total'))['total']
            
            # Répartition des ventes par plat
            repartition_par_plat = CommandePlat.objects.filter(commande__in=commandes).values('plat__nom').annotate(
                quantite_vendue=Sum('quantite'),
                montant_total=Sum(F('quantite') * F('plat__prix'), output_field=FloatField())
            )
            
            # Plats les plus populaires
            plats_populaires = repartition_par_plat.order_by('-quantite_vendue')[:5]
            
            # Variations des ventes
            variations_ventes = commandes.annotate(day=F('date_commande__date')).values('day').annotate(
                total=Sum('montant_total')
            ).order_by('day')
            
            # Revenus par catégorie
            revenus_par_categorie = CommandePlat.objects.filter(commande__in=commandes).values('plat__categorie__name').annotate(
                montant_total=Sum(F('quantite') * F('plat__prix'), output_field=FloatField())
            )
        
        except DatabaseError as e:
            error_message = f"Erreur lors de la récupération des données : {e}"
        except Exception as e:
            error_message = f"Une erreur inattendue est survenue : {e}"

    context = {
        'form': form,
        'ventes_totales': ventes_totales,
        'repartition_par_plat': repartition_par_plat,
        'plats_populaires': plats_populaires,
        'variations_ventes': variations_ventes,
        'revenus_par_categorie': revenus_par_categorie,
        'date_unique': date_unique,
        'error_message': error_message
    }
    return render(request, 'finance/ventes.html', context)

@login_required
def generer_rapport(request):
    # Assurez-vous de définir date_debut et date_fin avant d'utiliser ces variables
    date_debut = make_aware(datetime.combine(now().date(), time.min))
    date_fin = make_aware(datetime.combine(now().date(), time.max))

    commandes = Commande.objects.filter(
        caissier_confirme=True,
        etat='Confirmée',
        date_commande__range=[date_debut, date_fin]
    )

    # Calculer les différentes statistiques
    ventes_totales = commandes.aggregate(total=Sum('montant_total'))['total'] or 0
    
    repartition_par_plat = CommandePlat.objects.filter(commande__in=commandes).values('plat__nom').annotate(
        quantite_vendue=Sum('quantite'),
        montant_total=Sum(F('quantite') * F('plat__prix'), output_field=FloatField())
    )
    
    plats_populaires = repartition_par_plat.order_by('-quantite_vendue')[:5]
    
    variations_ventes = commandes.annotate(day=F('date_commande__date')).values('day').annotate(
        total=Sum('montant_total')
    ).order_by('day')
    
    revenus_par_categorie = CommandePlat.objects.filter(commande__in=commandes).values('plat__categorie__name').annotate(
        montant_total=Sum(F('quantite') * F('plat__prix'), output_field=FloatField())
    )
    
    # Exclure la marge bénéficiaire et les coûts et dépenses
    context = {
        'ventes_totales': ventes_totales,
        'repartition_par_plat': repartition_par_plat,
        'plats_populaires': plats_populaires,
        'variations_ventes': variations_ventes,
        'revenus_par_categorie': revenus_par_categorie,
        'date_unique': now().date(),
    }
    
    return render(request, 'finance/rapport.html', context)

@login_required
def custom_500(request):
    template = loader.get_template('500.html')
    return HttpResponseServerError(template.render({}, request))
