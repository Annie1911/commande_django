from django.urls import path
from finance.views import *

urlpatterns = [
    path('ventes/', consulter_ventes, name='consulter_ventes'),
    path('rapport/', generer_rapport, name='generer_rapport'),
   
]

handler500 = 'finance.views.custom_500'
