from asgiref.wsgi import WsgiToAsgi
from app.flask_app.app import app as flask_app

# Wrap the Flask WSGI app as an ASGI app
app = WsgiToAsgi(flask_app)