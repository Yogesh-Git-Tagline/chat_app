from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/', consumers.MyConsumer.as_asgi())
]