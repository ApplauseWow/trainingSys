from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

from trainingSys.routing import websocket_urlpatterns

# ASGI协议下类似于WSGI的url
application = ProtocolTypeRouter({
    # 'websocket': URLRouter(
    #     websocket_urlpatterns
    # )
})