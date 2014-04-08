# cat is short for 'catalog' (or 'catalogue'), not category. This is the application that stores products (and their categories)

import example_logic_tier as base
import rdf_json, utils, urllib, hashlib
from rdf_json import URI
from base_constants import RDF, LDP, CE
from sus_constants import SUS, BG
from cat_import import CSVImporter
from threading import Thread

#import logging
#logging.basicConfig(level=logging.DEBUG)

MEMBER_IS_OBJECT                =   True
MEMBER_IS_SUBJECT               =   False

NAMESPACE_MAPPINGS = {SUS : 'sus'}
NAMESPACE_MAPPINGS.update(base.NAMESPACE_MAPPINGS)

class Domain_Logic(base.Domain_Logic):
    def namespace_mappings(self):
        return NAMESPACE_MAPPINGS
        
    def get_document(self):
        if self.namespace == 'cat' and (self.document_id == 'products' or self.document_id == 'categories' or self.document_id == 'stores' or self.document_id == 'blogs'):
            # these are 'made up' resources that are not in the database but are manufactured here.
            if self.user is None:
                return (401, None, None)
            else:
                url_template = self.document_url() + '{}'
                membership_predicate = {
                    'products'   : SUS+'hasProduct',
                    'stores'     : SUS+'hasStore',
                    'categories' : SUS+'hasCategory',
                    'blogs'      : BG+'hasBlog',
                    } [self.document_id]
                membership_resource = self.document_url()
                document = self.create_container(url_template, membership_resource, membership_predicate, MEMBER_IS_OBJECT) 
                status, document = self.complete_result_document(document)
                return [status, [], document]
        else:
            return super(Domain_Logic, self).get_document()

    def complete_result_document(self, document):
        # in this section we add any calculated triples
        document_url = document.graph_url    
        types = document.getValues(RDF+'type')
        if URI(SUS+'OnlineStore') in types:
            document.add_triples(document_url, CE+'user', URI(self.user)) 
            document.add_triples(self.user, SUS+'cart', URI('/cart/current' + hashlib.sha224(self.user).hexdigest()))
            self.add_owned_container(document, SUS+'categories', 'categories', SUS+'store')
        if URI(SUS+'Category') in types:
            self.add_owned_container(document, SUS+'categoryProducts', 'products', SUS+'category')                      
        if URI(SUS+'BackOffice') in types: # add the triples for the store itself
            #the stored representation of the back_office does not reference the store, but the reference and store triples are added here
            self.add_resource_triples(document, document_url, SUS+'backOffice', MEMBER_IS_SUBJECT) 
            store_url = document.getSubject(SUS+"backOffice", None, document_url)
            document.add_triples(document_url, SUS+'store', store_url)
        return super(Domain_Logic, self).complete_result_document(document)

    def complete_document_for_container_insertion(self, document, container):
        container_url = self.request_url()
        if container.getValue(LDP+'hasMemberRelation', subject=container_url) == SUS+'categoryProducts': 
            # the standard processing in the superclass will add the new ProductDescription to the category. we want to add the product itself instead
            if not document.getValue(RDF+'type'):
                raise ValueError('must provide a type')
            category_url = container.getValue(LDP+'membershipResource', subject=container_url)
            product_url = document.getValue(SUS+'describes')
            document.add_triple('#product', SUS+'categoryProducts', {'type':'uri', 'value':product_url})
        elif container.getValue(LDP+'isMemberOfRelation', subject=container_url) == SUS+'hasProduct':
            # the standard processing in the superclass will add the new ProductDescription to the site. We want to add the product itself instead
            if not document.getValue(RDF+'type'):
                raise ValueError('must provide a type')
            store_url = container.getValue(LDP+'membershipResource', subject=container_url)
            product_url = document.getValue(SUS+'describes')
            document.add_triple(store_url, SUS+'hasProduct', {'type':'uri', 'value':product_url})
        else:
            return super(Domain_Logic, self).complete_document_for_container_insertion(document, container)
            
    def complete_document_for_storage_insertion(self, document):
        document_url = document.graph_url
        types = document.getValues(RDF+'type', [], document_url)
        if URI(SUS+'OnlineStore') in types: # When we create an OnlineStore, we also create a front and back office for it
            back_office = rdf_json.RDF_JSON_Document({'': {RDF+'type' : URI(SUS+'BackOffice')}}, '')
            status, headers, result = self.create_document(back_office)
            if status != 201: raise Exception
            back_office_url = base.get_header('Location', headers)
            document.add_triples('', {SUS+'backOffice': URI(back_office_url)})
            #If there is a system failure before insertion of the OnlineStore, then the back_office will be a harmless orphan not linked to anything
            #The stored representation of the back_office does not reference the store (which could fail to get created), but a triple that references the store 
            #is calculated at runtime on GET and added to the representation. See complete_result_document method for details
        return super(Domain_Logic, self).complete_document_for_storage_insertion(document)
        
    def execute_action(self, body):
        #TODO: check if post location is valid and body is a form
        form = body
        if 'file_to_import' in form:
            item = form["file_to_import"]
            if item.file and (item.headers['Content-type'] == 'application/vnd.ms-excel' or item.headers['Content-type'] == 'text/csv'):
                status, headers, document = self.recursive_get_document()
                if status == 200:
                    if document.getValue(RDF+'type') == URI(SUS+'BackOffice'):
                        store = document.getValue(SUS+'store')
                        cat_categories_post_url = str(document.getValue(SUS+'categories', None, store))
                        cat_products_post_url = str(utils.construct_url(self.request_hostname, self.tenant, self.namespace, 'products'))
                        id_prefix = self.document_id + '-'
                        thread = Thread(target = threaded_import_products, args = (item, cat_categories_post_url, cat_products_post_url, id_prefix, self.user))
                        thread.start()
                        return (202, [], 'Product import started ...')
        return super(Domain_Logic, self).execute_action(body)

def threaded_import_products(item, cat_categories_post_url, cat_products_post_url, id_prefix, user):
    csv_importer = CSVImporter(cat_categories_post_url, cat_products_post_url, id_prefix, user)
    csv_importer.import_csv_products(item.file)
    print "done import."
