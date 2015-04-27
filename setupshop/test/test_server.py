import os, sys, logging

sys.path.append('../../../lda-serverlib/logiclibrary')
sys.path.append('../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../lda-clientlib/python')
sys.path.append('../../../lda-clientlib/python/test')
sys.path.append('../src')

from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIServer
from SocketServer import ThreadingMixIn

class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
    """Handle requests in a separate thread."""

SERVER_NAME = 'setupshop'
    
os.environ['APP_NAME'] = SERVER_NAME
os.environ['MONGODB_DB_HOST'] = 'localhost' # 'ec2-50-19-190-34.compute-1.amazonaws.com'
os.environ['MONGODB_DB_PORT'] = '27017'
os.environ['HOSTINGSITE_HOST'] = 'hostingsite.localhost:3001'
os.environ['SYSTEM_HOST'] = '127.0.0.1:3001'
 
from ld4apps.logic_server import application
from werkzeug.wsgi import SharedDataMiddleware

application = SharedDataMiddleware(application, {
    '/setupshop': os.path.join(os.path.dirname(__file__), '../wsgi/static/setupshop'),
})

PORT = 3006
httpd = make_server('0.0.0.0', PORT, application, server_class=ThreadedWSGIServer)
print 'test %s initiated on host: localhost port: %d' % (SERVER_NAME, PORT)
logging.basicConfig(level=logging.DEBUG)
httpd.serve_forever()