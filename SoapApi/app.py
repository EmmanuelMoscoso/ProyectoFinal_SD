from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from controllers.controllers import ResourceService
from infrastructure.postgres import initialize_database

# Initialize the database
initialize_database()

# Set up the SOAP application
application = Application(
    [ResourceService],
    tns='soap.api',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("SOAP server running on http://0.0.0.0:8000")
    server.serve_forever()
