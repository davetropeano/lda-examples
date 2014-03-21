import os, logging
from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIServer
from SocketServer import ThreadingMixIn

class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
    """Handle requests in a separate thread."""

APP_NAME = 'tutorial'
PORT = 3007
    
os.environ['APP_NAME'] = APP_NAME
os.environ['MONGODB_DB_HOST'] = 'localhost'
os.environ['MONGODB_DB_PORT'] = '27017'
os.environ['CHECK_ACCESS_RIGHTS'] = 'False'
 
from logic_server import application
from werkzeug.wsgi import SharedDataMiddleware

application = SharedDataMiddleware(application, {
    '/clientlib': os.path.join(os.path.dirname(__file__), '../../lda-clientlib'),
    '/tutorial': os.path.join(os.path.dirname(__file__), 'static'),
})

httpd = make_server('0.0.0.0', PORT, application, server_class=ThreadedWSGIServer)
print '%s application initiated on host: localhost port: %d' % (APP_NAME, PORT)
logging.basicConfig(level=logging.DEBUG)
httpd.serve_forever()