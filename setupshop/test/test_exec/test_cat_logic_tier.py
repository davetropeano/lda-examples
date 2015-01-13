import sys
sys.path.append('../../../../lda-serverlib')
sys.path.append('../../../../lda-serverlib/logiclibrary')
sys.path.append('../../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../../lda-clientlib/python')
sys.path.append('../../../../lda-clientlib/python/test')
sys.path.append('../../src')
sys.path.append('../../test')

import requests, json, jwt
from rdf_json import URI, BNode, RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
from base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
from sus_constants import SUS
import pytest
import test_helper
from test_helper import USER1_URL, USER2_URL, HS_HOSTNAME, ac_container_url

mt_container_url = 'http://%s/mt' % HS_HOSTNAME
mt_sites_url = 'http://%s/mt/sites' % HS_HOSTNAME
mt_capabilities_url = 'http://%s/mt/capabilities' % HS_HOSTNAME

CS_TENANT = 'cloudsupplements'
CS_HOSTNAME = CS_TENANT + '.' + 'localhost:3001'
cs_ac_app_url = 'http://%s/ac' % CS_HOSTNAME
cs_cat_app_url = 'http://%s/cat' % CS_HOSTNAME
cs_cat_products_url = 'http://%s/cat/products' % CS_HOSTNAME
cs_cat_categories_url = 'http://%s/cat/categories' % CS_HOSTNAME
cs_cat_stores_url = 'http://%s/cat/stores' % CS_HOSTNAME
cs_cart_url = 'http://%s/cart' % CS_HOSTNAME


def test_basic_crud():
    post_body = {
        '' : {
            RDF+'type': URI(SUS+'Category'),
            CE+'id': 'just_some_id',
            DC+'title': 'test category',
        }
    }

    patch_prop = DC+'title'
    patch_val = 'updated test category'
    test_helper.container_crud_test(cs_cat_categories_url, post_body, patch_prop, patch_val)

'''
def test_user_create_site_store(account_user1, store_capability):
    """
    :param account_user1: RDF_Document passed in via py.test.  Even though it's not used it's needed to ensure user1 exists
    :param store_capability: RDF_Document passed in via py.test
    verify that a user create an enhancement for a site with a capability
    """

    #test_helper.pp.pprint(account_user1)
    body = {
        '': {
            CE+'site_id': TENANT_TEST,
            CE+'public': True,
            RDF+'type': {'type': 'uri', 'value': CE+'Site'},
            CE+'site_home': URI(store_url),
            DC+'title': 'Cloud Supplements Site',
            CE+'improvements': [URI(store_url), URI(blogservice_url)]
        }
    }

    store_capability_url = store_capability.default_subject()
    store_capability_type = store_capability.get_value(CE+'improvement_type')
    body = {
        '': {
            #RDF+'type': URI(SUS+'OnlineStore'),
            #RDF+'type': URI('/types/OnlineStore'),  # the type must match the improvement_type of the capability
            RDF+'type': store_capability_type,
            DC+'title': 'Test Store',
            CE+'capability': URI(store_capability_url)
        }
    }
    test_helper.create(cs_cat_app_url, body, ADMIN_USER)
'''

@pytest.fixture(scope="session")
def store_capability():
    post_body = {
        '': {
            RDF+'type': URI(CE+'Capability'),
            DC+'title': 'Example Capability',
            CE+'improvement_container': URI('/cat/stores'),
            CE+'improvement_type': URI('/types/OnlineStore')
        }
    }
    capability_rdoc = test_helper.create(mt_capabilities_url, post_body, username=ADMIN_USER)
    return capability_rdoc

# this is for working with tests while building them
if __name__ == "__main__":
    test_basic_crud()
    pass