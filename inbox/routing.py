# chat/routing.py
from django.urls import re_path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    # (?P<rooom_name>\w+)/
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]

