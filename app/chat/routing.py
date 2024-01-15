from django.urls import re_path

from chat.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/view/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]
