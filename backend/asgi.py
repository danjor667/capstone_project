"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import PatientUpdateConsumer
from .socketio_server import socketio_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

websocket_urlpatterns = [
    path('ws/', PatientUpdateConsumer.as_asgi()),
]

django_asgi_app = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] == 'http' and scope['path'].startswith('/socket.io/'):
        await socketio_app(scope, receive, send)
    elif scope['type'] == 'websocket':
        websocket_app = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        await websocket_app(scope, receive, send)
    else:
        await django_asgi_app(scope, receive, send)
