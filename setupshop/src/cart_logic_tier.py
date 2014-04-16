import urlparse
import operation_primitives
import example_logic_tier as base
import utils
import rdf_json
from base_constants import RDF, CE, AC
from sus_constants import SUS, BG
from base_constants import URL_POLICY as url_policy
#import logging
#logging.basicConfig(level=logging.DEBUG)

MEMBER_IS_OBJECT                =   True
MEMBER_IS_SUBJECT               =   False

class Domain_Logic(base.Domain_Logic):
    
    def get_document(self, primitive=False):
        if self.document_id.startswith("current"):
            #it must be '/cart/current<userUrlHash>' or '/cart/current<userUrlHash>/cartItems'
            cart_subject = url_policy.construct_url(self.request_hostname, self.tenant, self.namespace, self.document_id) 
            cart = rdf_json.RDF_JSON_Document({ 
                    cart_subject:{ 
                                    RDF+"type": rdf_json.URI("http://setupshop.me/ns#Cart"),
                                    CE+'user': rdf_json.URI(self.user)
                                    } 
            }, cart_subject)
            self.complete_result_document(cart)                        
            return 200, [], cart
        return super(Domain_Logic, self).get_document()
                    
    def complete_result_document(self, document):
        types = document.getValues(RDF+'type')
        if rdf_json.URI(SUS+'Cart') in types:
            #it must be '/cart/current<userUrlHash>'
            self.add_owned_container(document, SUS+'cartItems', 'cartItems', SUS+'cart')            
        return super(Domain_Logic, self).complete_result_document(document)
    
    def default_resource_group(self):
        if self.namespace == 'cart':
            return url_policy.construct_url(self.request_hostname, self.tenant, self.namespace)
        return super(Domain_Logic, self).default_resource_group()
