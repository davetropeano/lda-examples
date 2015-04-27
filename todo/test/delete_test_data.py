import requests
from ld4apps.base_constants import ADMIN_USER
from ld4apps.test.test_utils import DELETE_HEADERS

DATASERVER_HOSTNAME = 'localhost:3007'

items_container_url = 'http://%s/items' % DATASERVER_HOSTNAME

def run():
    requests.delete(items_container_url, headers=DELETE_HEADERS)

if __name__ == '__main__':
    run()
