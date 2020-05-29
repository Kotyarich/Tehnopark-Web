from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from . import consumers


channel_routing = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r"^nf/$", consumers.NotificationConsumer),
        ])
    ),
})
