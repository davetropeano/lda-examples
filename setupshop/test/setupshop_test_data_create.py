#
# Create setupshop sample data.
#
import os, requests, json, sys
from rdf_json import URI, RDF_JSON_Document, RDF_JSON_Encoder, rdf_json_decoder
from cat_import import CSVImporter
from base_constants import CE, RDF, DC, AC, AC_R, AC_C, AC_ALL, ADMIN_USER, ANY_USER
from sus_constants import SUS, BG
from cryptography import encode_jwt

encoded_jwt = encode_jwt({'user':ADMIN_USER})
CONTENT_RDF_JSON_HEADER = {
    'Content-type' : 'application/rdf+json+ce',
    'Cookie' : 'SSSESSIONID=%s' % encoded_jwt,
    'ce-post-reason' : 'ce-create'
    }

#DATASERVER_HOST = 'cloudapps4.me'
DATASERVER_HOST = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else 'localhost:3001' 

if 'DATASERVER_HOST' in os.environ:
    DATASERVER_HOST = os.environ['DATASERVER_HOST']

if DATASERVER_HOST.startswith('localhost'):
    HOSTINGSITE_HOST = DATASERVER_HOST
else:
    HOSTINGSITE_HOST = 'hostingsite.' + DATASERVER_HOST

CS_SITE_ID = 'cloudsupplements'
CS_HOST = 'cloudsupplements.%s' % DATASERVER_HOST

sites_post_url = 'http://%s/mt/sites' % HOSTINGSITE_HOST
hs_mt_app_url = 'http://%s/mt' % HOSTINGSITE_HOST
mt_capabilities_url = 'http://%s/mt/capabilities' % HOSTINGSITE_HOST

hs_ac_app_url = 'http://%s/ac' % HOSTINGSITE_HOST
cs_ac_app_url = 'http://%s/ac' % CS_HOST
cs_cat_app_url = 'http://%s/cat' % CS_HOST
cs_cat_products_url = 'http://%s/cat/products' % CS_HOST
cs_cat_categories_url = 'http://%s/cat/categories' % CS_HOST
cs_cat_stores_url = 'http://%s/cat/stores' % CS_HOST
cs_cart_url = 'http://%s/cart' % CS_HOST

file_path = os.path.dirname(os.path.abspath(__file__))
csv_file_name = os.path.join(file_path, 'data/vitalmax.csv')

def run():
    requests.delete(hs_mt_app_url, headers=CONTENT_RDF_JSON_HEADER)
    requests.delete(cs_cat_app_url, headers=CONTENT_RDF_JSON_HEADER)
    requests.delete(hs_ac_app_url, headers=CONTENT_RDF_JSON_HEADER)
    requests.delete(cs_ac_app_url, headers=CONTENT_RDF_JSON_HEADER)
    requests.delete(cs_cart_url, headers=CONTENT_RDF_JSON_HEADER)

    body = {
        '' : {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who' : [
                URI(ADMIN_USER),
                URI('http://martin-nally.name'),
                URI('http://frank-budinsky.name'),
                URI('http://dave-tropeano.name'),
                URI('http://paul-matchen.name'),
                URI('http://mark-archer.name')
                ],
            AC+'may' : [ URI('#permission_1') ],
            },
        '#permission_1' : {
            AC+'do' : AC_ALL,
            AC+'to' : [ URI('/'), URI('/mt/cloudsupplements') ]
            }
        }
    r = requests.post(hs_ac_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE user group! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)

    body['#permission_1'][AC+'to'] = URI('/')
    r = requests.post(cs_ac_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE access control! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)

    body = {
        '' : {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who' : [
                URI(ANY_USER)
                ],
            AC+'may' : [
                URI('#permission_1'),
                URI('#permission_2')
                ]
            },
        '#permission_1' : {
            AC+'do' : AC_R,
            AC+'to' : [ URI('/') ]
            },
        '#permission_2' : {
            AC+'do' : AC_C,
            AC+'to' : [ URI('/account'), URI('/mt/sites'), URI('/cart') ]
            }
        }
    r = requests.post(hs_ac_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE user group! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)

    r = requests.post(cs_ac_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE access control! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)

    body = {
        '' : {
            RDF+'type': URI(CE+'Capability'),
            DC+'title': 'IBM Shopping Capability',
            CE+'improvement_container': URI('/cat/stores'),
            CE+'improvement_type': URI(SUS+'OnlineStore')
            }
        }
    r = requests.post(mt_capabilities_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE Shopping Service Provider! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
    store_capability_url = r.headers['location']
    store_capability = RDF_JSON_Document(json.loads(r.text, object_hook=rdf_json_decoder), store_capability_url)

    body = {
        '' : {
            RDF+'type': URI(CE+'Capability'),
            DC+'title': 'IBM Blogging Capability',
            CE+'improvement_container': URI('/cat/blogs'),
            CE+'improvement_type': URI(BG+'BlogService')
            }
        }
    r = requests.post(mt_capabilities_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE Blogging service provider! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
    blog_capability_url = r.headers['location']
    blog_capability = RDF_JSON_Document(json.loads(r.text, object_hook=rdf_json_decoder), blog_capability_url)

    body = {
        '' : {
            RDF+'type': URI(SUS+'OnlineStore'),
            DC+'title': 'Cloud Supplements Shop, LLC',
            CE+'capability': URI(store_capability_url)
            }
        }
    r = requests.post(cs_cat_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE Online Store! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)

    store_url = r.headers['location']
    store = RDF_JSON_Document(json.loads(r.text, object_hook=rdf_json_decoder), store_url)
    cs_cat_categories_url = str(store.getValue(SUS+'categories'))
    backoffice_url = str(store.getValue(SUS+'backOffice'))
    id_prefix = backoffice_url[backoffice_url.rfind('/')+1:] + '-'

    body = {
        '' : {
            RDF+'type': URI(BG+'BlogPost'),
            DC+'title': 'First Post',
            BG+'content': 'Hello. This is the first blog post',
            }
        }
    r = requests.post(cs_cat_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE BLOG POST! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
    blogpost_url = r.headers['location']

    body = {
        '' : {
            RDF+'type': URI(BG+'Blog'),
            DC+'title': 'News',
            BG+'blog_posts': [ URI(blogpost_url) ]
            }
        }
    r = requests.post(cs_cat_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE BLOG! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
    blog_url = r.headers['location']

    body = {
        '' : {
            RDF+'type': URI(BG+'BlogService'),
            DC+'title': 'Cloud Supplements Blogging Service',
            BG+'blogs': [ URI(blog_url)],
            CE+'capability': URI(blog_capability_url)
            }
        }
    r = requests.post(cs_cat_app_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE BLOG SERVICE! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
    blogservice_url = r.headers['location']

    body = {
        '' : {
            CE+'site_id' : CS_SITE_ID,
            CE+'public' : True,
            RDF+'type': {'type': 'uri', 'value' : CE+'Site'},
            CE+'site_home' : URI(store_url),
            DC+'title': 'Cloud Supplements Site',
            CE+'improvements' : [URI(store_url), URI(blogservice_url)]
            }
        }
    r = requests.post(sites_post_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls = RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE SITE! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
    site_url = r.headers['location']
    site = RDF_JSON_Document(json.loads(r.text, object_hook=rdf_json_decoder), site_url)
    site_service_url = str(site.getValue(CE+'services'))

    csv_importer = CSVImporter(cs_cat_categories_url, cs_cat_products_url, id_prefix)
    if csv_importer.import_products(csv_file_name):
        print 'Done.'
    else:
        print 'Data Import FAILED!'

if __name__ == '__main__':
    run()
