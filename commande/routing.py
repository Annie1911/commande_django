# commande/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/commandes/', consumers.CommandeConsumer.as_asgi()),
]
