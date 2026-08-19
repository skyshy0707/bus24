"""
ASGI config for bus_lead project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

# Устанавливаем DJANGO_SETTINGS_MODULE ДО любых импортов Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_lead.settings')

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from api.ws import Chat

django_schema = get_asgi_application()

# Отладка WebSocket маршрутов
import logging
logger = logging.getLogger(__name__)

print("LOADING ASGI APPLICATION...")
print(f"Chat consumer: {Chat}")
print(f"Chat type: {type(Chat)}")

# Создаём ASGI application для Chat
chat_app = Chat.as_asgi()
logger.info(f"chat_app: {chat_app}")
logger.info(f"chat_app type: {type(chat_app)}")

# Создаём URLRouter с отладкой
websocket_urlpatterns = [
    path("ws/api/messages", chat_app),
]
logger.info(f"WebSocket URL patterns: {websocket_urlpatterns}")

websocket_router = URLRouter(websocket_urlpatterns)
logger.info(f"WebSocket router: {websocket_router}")

application = ProtocolTypeRouter({
    "http": django_schema,
    "websocket": AuthMiddlewareStack(websocket_router),
})

logger.info("ASGI application configured successfully")
