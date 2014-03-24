import base64, requests
import json, os
from cryptography import encode_jwt

USER_URL = 'http://ibm.com/user/Frank'
SIGNATURE_PUBLIC_KEY = 'our little secret'
encoded_jwt = encode_jwt({'user':USER_URL})
AUTH_HEADER = { 'Cookie' : 'SSSESSIONID=%s' % encoded_jwt }

DATASERVER_HOSTNAME = 'localhost:3001'
if 'SERVICE_HOSTNAME' in os.environ:
    DATASERVER_HOSTNAME = os.environ['SERVICE_HOSTNAME']
TS_HOSTNAME = 'testsite.%s' % DATASERVER_HOSTNAME

ts_ac_app_url = 'http://%s/ac' % TS_HOSTNAME
ts_mt_app_url = 'http://%s/mt' % TS_HOSTNAME
ts_cat_app_url = 'http://%s/cat' % TS_HOSTNAME

def run():
    requests.delete(ts_ac_app_url, headers=AUTH_HEADER)
    requests.delete(ts_mt_app_url, headers=AUTH_HEADER)
    requests.delete(ts_cat_app_url, headers=AUTH_HEADER)

if __name__ == '__main__':
    run()
