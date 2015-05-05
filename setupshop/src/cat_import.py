import csv, json, requests, jwt

import ld4apps.rdf_json as rdf_json
from ld4apps.rdf_json import URI
from ld4apps.base_constants import RDF, DC, CE, ADMIN_USER

from sus_constants import SUS

##################################################
# TODO Move the following to a reusable place. Temporarily copied from test_utils
SHARED_SECRET = 'our little secret'
encoded_signature = jwt.encode({'user': ADMIN_USER}, SHARED_SECRET, 'HS256')
POST_HEADERS = {
    'Content-type': 'application/rdf+json+ce', 
    'Cookie': 'SSSESSIONID=%s' % encoded_signature, 
    'ce-post-reason': 'ce-create' 
    }
##################################################

class CSVImporter():
    def __init__(self, cat_categories_url, cat_products_url, id_prefix, user=ADMIN_USER):
        self.cat_categories_url = cat_categories_url
        self.cat_products_url = cat_products_url
        self.id_prefix = id_prefix
        self.categories = {}
        self.products = {}
        self.headers = POST_HEADERS

    def import_products(self, csv_file_name):
        infile = open(csv_file_name)
        return self.import_csv_products(infile)
        
    def import_csv_products(self, infile):
        reader = csv.reader(infile.read().splitlines())
        key_map = {}
        first = True
        for row in reader:
            if first:
                for i in range(len(row)):
                    key_map[row[i]] = i
                first = False
                continue
            category_key = row[key_map['Category']]
            if category_key not in self.categories:
                category_document = CategoryDocument(key_map, row, self.cat_categories_url, self.id_prefix, self.headers)
                self.categories[category_key] = category_document
            else:
                category_document = self.categories[category_key]
            category_url = category_document.get_resource()
            if category_url is None:
                return False
            product_key = row[key_map['Title']]
            if product_key not in self.products:
                product_document = ProductDocument(key_map, row, category_url, self.cat_products_url, self.id_prefix, self.headers)
                self.products[product_key] = product_document
            else:
                product_document = self.products[product_key]
            product_document.add_variant(row)
        for product in self.products.values():
            #print json.dumps(product.document, indent=4)
            if product.get_resource() is None:
                return False
        return True # Success!

class ResourceDocument:
    def __init__(self, key_map, post_url, headers):
        self.key_map = key_map
        self.post_url = post_url
        self.resource_url = None
        self.headers = headers
        
    def get_resource(self):
        if self.resource_url is None:
            r = requests.post(self.post_url, headers=self.headers, data=json.dumps(self.document, cls=rdf_json.RDF_JSON_Encoder), verify=False)
            if r.status_code == 201:
                print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
                self.resource_url = r.headers['location']
            elif r.status_code == 409:
                print '######## WARNING, resource already POSTed: %s, status: %d' % (r.headers['location'], r.status_code)
                self.resource_url = r.headers['location']
            else:
                print '######## FAILED TO CREATE Resource! ' + r.text
        return self.resource_url

class CategoryDocument(ResourceDocument):
    def __init__(self, key_map, row, post_url, id_prefix, headers):
        ResourceDocument.__init__(self, key_map, post_url, headers)
        self.document = self.make_category(row, id_prefix)
        
    def make_category(self, row, id_prefix):
        category = { \
            '' : {
                RDF+'type': URI(SUS+'Category'),
                CE+'id': id_prefix + row[self.key_map['Category']].lower().replace(' ', '-'),
                DC+'title': row[self.key_map['Category']],
                SUS+'image_source': URI(row[self.key_map['Image Src']]),
                SUS+'image_alt_text': row[self.key_map['Image Alt Text']]
                }
            }
        return category

class ProductDocument(ResourceDocument):
    def __init__(self, key_map, row, category_url, post_url, id_prefix, headers):
        ResourceDocument.__init__(self, key_map, post_url, headers)
        self.document = self.make_product(row, category_url, id_prefix)
        self.variant_count = 1
        self.image_count = 1
        self.images = {}
 
    def add_variant(self, row):
        k = "#variant-%s" % self.variant_count
        self.variant_count += 1
        v = self.make_variant(row)
        self.document[k] = v
        self.document['#product'][SUS+'variants'].append(URI(k))
        image_key = row[self.key_map['Image Src']]
        if image_key not in self.images:
            k = "#image-%s" % self.image_count
            self.image_count += 1
            self.images[image_key] = k
            v = self.make_image(row)
            self.document[k] = v
            self.document['#product'][SUS+'images'].append(URI(k))
        for i in range(1,3):
            option_name = row[self.key_map['Option%s Name' % i]]
            if option_name == '':
                continue
            k = "#option-%s" % i
            if k not in self.document:
                v = self.make_option(option_name, i)
                self.document[k] = v
                self.document['#product'][SUS+'options'].append(URI(k))
            option_value = row[self.key_map['Option%s Value' % i]]
            value_list = self.document[k][SUS+'option_values']
            if option_value not in value_list:
                value_list.append(option_value)

    def make_product(self, row, category_url, id_prefix):
        product = {
            '': {
                RDF+'type': URI(SUS+'ProductDescription'),
                CE+'id': id_prefix + row[self.key_map['Handle']]
                },
            '#product': {
                RDF+'type': URI(SUS+'Product'),
                RDF+'isDefinedBy': URI(''),
                DC+'title': row[self.key_map['Title']],
                DC+'description': row[self.key_map['Description']],
                SUS+'vendor': row[self.key_map['Vendor']],
                SUS+'category': [URI(category_url)],
                SUS+'tags': [row[self.key_map['Tags']]],
                SUS+'featured_image': URI('#image-1'),
                SUS+'images': [],
                SUS+'options': [],
                SUS+'variants': []
                }
             }
        return product

    def get_variant_title(self, row):
        title = row[self.key_map['Option1 Value']]
        option2_value = row[self.key_map['Option2 Value']]
        if option2_value != '':
            title += '/' + option2_value
        option3_value = row[self.key_map['Option3 Value']]
        if option3_value != '':
            title += '/' + option3_value
        return title    
     
    def make_variant(self, row):
        variant = {
            RDF+'type': URI(SUS+'Variant'),
            DC+'title': self.get_variant_title(row),
            DC+'description': row[self.key_map['Description']],
            SUS+'sku': row[self.key_map['Variant SKU']],
            SUS+'inventory_tracker': row[self.key_map['Variant Inventory Tracker']],
            SUS+'inventory_qty': int(row[self.key_map['Variant Inventory Qty']]),
            SUS+'inventory_policy': row[self.key_map['Variant Inventory Policy']],
            SUS+'fulfillment_service': row[self.key_map['Variant Fulfillment Service']],
            SUS+'price': int(100*float(row[self.key_map['Variant Price']])),
            SUS+'compare_at_price': int(100*float(row[self.key_map['Variant Compare At Price']])),
            SUS+'requires_shipping': row[self.key_map['Variant Requires Shipping']]=='TRUE',
            SUS+'taxable': row[self.key_map['Variant Taxable']]=='TRUE',
            SUS+'barcode': row[self.key_map['Variant Barcode']]
            }
        return variant
    
    def make_image(self, row):
        image = {
            RDF+'type': URI(SUS+'AnnotatedImage'),
            SUS+'image_source': URI(row[self.key_map['Image Src']]),
            SUS+'image_alt_text': row[self.key_map['Image Alt Text']]
            }
        return image
    
    def make_option(self, option_name, option_index):
        option = {
            RDF+'type': URI(SUS+'Option'),
            SUS+'option_name': option_name,
            SUS+'option_index': option_index,
            SUS+'option_values': []
            }
        return option
