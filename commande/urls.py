from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('consulter_menu', views.consulter_menu, name='consulter_menu'),
    path('ajouter_au_panier/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('modifier_commande/<int:commande_plat_id>/', views.modifier_commande, name='modifier_commande'),
    path('consulter_panier/', views.consulter_panier, name='consulter_panier'),
    path('confirmer_commande/<int:commande_id>/', views.confirmer_commande, name='confirmer_commande'),
    path('confirmation/<int:commande_id>/', views.confirmation, name='confirmation'),
    path('commande_annuler/<int:commande_id>/', views.commande_annuler, name='commande_annuler'),
]
