from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_ingredients, name='liste_ingredients'),
    path('ajouter/', views.ajouter_ingredient, name='ajouter_ingredient'),
    path('modifier/<int:pk>/', views.modifier_ingredient, name='modifier_ingredient'),
    path('supprimer/<int:pk>/', views.supprimer_ingredient, name='supprimer_ingredient'),
    path('ajuster/<int:pk>/', views.ajuster_stock, name='ajuster_stock'),
    path('historique_mouvements_stock/', views.historique_mouvements_stock, name='historique_mouvements_stock'),

]
