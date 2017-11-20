from channels.routing import route
from gingr.consumers import ws_receive, ws_connect, ws_disconnect

# websockets version of "urlpatterns"
channel_routing = [
	route('websocket.receive', ws_receive),
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]