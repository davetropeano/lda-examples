import base64, requests
import json, os
from test_utils import DELETE_HEADERS

DATASERVER_HOSTNAME = 'localhost:3001'
if 'SERVICE_HOSTNAME' in os.environ:
    DATASERVER_HOSTNAME = os.environ['SERVICE_HOSTNAME']
TS_HOSTNAME = 'testsite.%s' % DATASERVER_HOSTNAME

ts_ac_app_url = 'http://%s/ac' % TS_HOSTNAME
ts_mt_app_url = 'http://%s/mt' % TS_HOSTNAME
ts_cat_app_url = 'http://%s/cat' % TS_HOSTNAME

def run():
    requests.delete(ts_ac_app_url, headers=DELETE_HEADERS)
    requests.delete(ts_mt_app_url, headers=DELETE_HEADERS)
    requests.delete(ts_cat_app_url, headers=DELETE_HEADERS)

if __name__ == '__main__':
    run()
