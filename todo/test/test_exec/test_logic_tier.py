import sys
sys.path.append('../../../../lda-serverlib')
sys.path.append('../../../../lda-serverlib/logiclibrary')
sys.path.append('../../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../../lda-clientlib/python')
sys.path.append('../../../../lda-clientlib/python/test')
sys.path.append('../../src')
sys.path.append('../../test')

import requests, json, jwt
from ld4apps.rdf_json import URI, BNode, RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
from ld4apps.base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
import pytest
import ld4apps.test.test_helper as test_helper
from test_helper import USER1_URL, USER2_URL, HS_HOSTNAME, ac_container_url

ITEMS_URL = "http://localhost:3007/items"

def test_basic_crud():
    post_body = {
        '' : {
            RDF+'type': URI('http://example.org/todo#Item'),
            DC+'title': 'test todo',
        }
    }

    patch_prop = DC+'title'
    patch_val = 'updated test todo'
    test_helper.container_crud_test(ITEMS_URL, post_body, patch_prop, patch_val)

# this is for working with tests while building them
if __name__ == "__main__":
    test_basic_crud()
    pass