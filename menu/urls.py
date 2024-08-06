from django.urls import path
from menu.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('commandes_reçu/', commandes_reçu, name='commandes_reçu'),
    path('annuler_commande/<int:commande_id>/',annuler_commande, name='annuler_commande'),
    path('gerer_menu/', gerer_menu, name='gerer_menu'),
    path('ajouter_plat/', ajouter_plat, name='ajouter_plat'),
    path('modifier_plat/<int:plat_id>/', modifier_plat, name='modifier_plat'),
    path('supprimer_plat/<int:plat_id>/', supprimer_plat, name='supprimer_plat'),
    path('gerer_categories/', gerer_categories, name='gerer_categories'),
    path('ajouter_categorie/', ajouter_categorie, name='ajouter_categorie'),
    path('modifier_categorie/<int:categorie_id>/', modifier_categorie, name='modifier_categorie'),
    path('supprimer_categorie/<int:categorie_id>/', supprimer_categorie, name='supprimer_categorie'),
    path('delete_all_plats_in_category/<int:category_id>/', delete_all_plats_in_category, name='delete_all_plats_in_category'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
