from django.urls import path
from .views import *

urlpatterns = [
    # autres urls
    path('detail_commande/<int:commande_id>/', detail_commande, name='detail_commande'),
    path('recevoir_commandes/', recevoir_commandes, name='recevoir_commandes'),
    path('confirmer_paiement/<int:commande_id>/', confirmer_paiement, name='confirmer_paiement'),
]
