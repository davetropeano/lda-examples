import requests
from base_constants import ADMIN_USER
from cryptography import encode_jwt

encoded_jwt = encode_jwt({'user':ADMIN_USER})
DELETE_HEADER = { 'Cookie' : 'SSSESSIONID=%s' % encoded_jwt }
DATASERVER_HOSTNAME = 'localhost:3007'

items_container_url = 'http://%s/items' % DATASERVER_HOSTNAME

def run():
    requests.delete(items_container_url, headers=DELETE_HEADER)

if __name__ == '__main__':
    run()
