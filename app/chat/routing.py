from django.urls import re_path

from chat.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/aprs_room/", ChatConsumer.as_asgi()),
]
