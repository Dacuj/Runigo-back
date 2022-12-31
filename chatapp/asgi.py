# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# application = get_asgi_application()





# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcribe.settings')

# application = get_asgi_application()




import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import inbox.routing
from channels.security.websocket import OriginValidator
from channels.security.websocket import AllowedHostsOriginValidator
# from inbox.custommiddleware import TokenAuthMiddleware



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


# application = ProtocolTypeRouter({
#     # "http": get_asgi_application(),
#     "websocket": AllowedHostsOriginValidator(
#         TokenAuthMiddleware(
#         # AuthMiddlewareStack(
#             URLRouter(
#                 chat.routing.websocket_urlpatterns
#             )
#         ),
#     ),
# })



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                inbox.routing.websocket_urlpatterns
            )
        ),
    ),
})



# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": OriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 inbox.routing.websocket_urlpatterns
#             )
#         ),
#         ['http://localhost:8000/'],
#     ),
# })
