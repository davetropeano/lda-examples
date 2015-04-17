#!/usr/bin/python
#
# This script creates, updates, and deletes Todo Items

import sys, requests, json

TDSERVICE_HOST = sys.argv[1] if len(sys.argv) > 1 else 'http://example.localhost:3007'
requests.delete(TDSERVICE_HOST+'/td') # start with clean DB
              
# Create Item #1
body = {
    "rdf_type": "http://example.org/todo#Item",
    "dc_title": "do the first thing"
}
r = requests.post(TDSERVICE_HOST+'/td/items', headers={'Content-type': 'application/json'}, data=json.dumps(body))
if r.status_code != 201: 
    print r.text
    sys.exit(1)
item1 = r.json()
item1_url = r.headers['Location']
print ">>> POSTed Item: "+item1_url
print json.dumps(item1, indent=4)

# Create Item #2
body = {
    "rdf_type": "http://example.org/todo#Item",
    "dc_title": "do a second thing"
}
r = requests.post(TDSERVICE_HOST+'/td/items', headers={'Content-type': 'application/json'}, data=json.dumps(body))
if r.status_code != 201: 
    print r.text
    sys.exit(1)
item2 = r.json()
item2_url = r.headers['Location']
print ">>> POSTed Item: "+item2_url
print json.dumps(item2, indent=4)

# Create Item #3
body = {
    "rdf_type": "http://example.org/todo#Item",
    "dc_title": "do a third thing"
}
r = requests.post(TDSERVICE_HOST+'/td/items', headers={'Content-type': 'application/json'}, data=json.dumps(body))
if r.status_code != 201: 
    print r.text
    sys.exit(1)
item3 = r.json()
item3_url = r.headers['Location']
print ">>> POSTed Item: "+item3_url
print json.dumps(item3, indent=4)

# Update Item #1
body = {
    "dc_title": "do the first thing - today!"
}
r = requests.patch(item1_url, headers={'Content-type': 'application/json', 'CE-Revision': item1['ce_revision']}, data=json.dumps(body))
if r.status_code != 200: 
    print r.text
    sys.exit(1)
item1 = r.json()
print ">>> PATCHed enabled for Feature: "+item1_url
print json.dumps(item1, indent=4)

# Delete Item #2   
r = requests.delete(item2_url)
if r.status_code != 200:
    print r.text
    sys.exit(1)
print ">>> DELETED Group: "+item2_url

# Get list of Items
r = requests.get(TDSERVICE_HOST+'/td/items', headers={'Accept': 'application/json'})
if r.status_code != 200: print r.text; sys.exit(1)
print ">>> GET Item List"
print json.dumps(r.json(), indent=4)
