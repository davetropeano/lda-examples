from ld4apps import lda
from flask import Flask, abort, request

app = Flask(__name__, static_url_path='')

@app.route('/td/items', methods=['GET'])
def items():
    document, status, headers = lda.get_virtual_container(request.environ, 'ce_item_of')
    if status != 200:
        abort(status)
    document, headers = lda.convert_to_requested_format(document, headers, request.environ)
    return document, status, headers

@app.route('/td/items', methods=['POST'])
def create_item():
    if request.json.get('rdf_type') != "http://example.org/todo#Item":
        abort(400)
    #TODO: add more validation
    document, status, headers = lda.create_document(request.environ, request.json, 'ce_item_of')
    if status != 201:
        abort(status)
    document, headers = lda.convert_to_requested_format(document, headers, request.environ)
    return document, status, headers

@app.route('/td/items/<i>', methods=['GET'])
def read_item(i):
    document, status, headers = lda.get_document(request.environ)
    if status != 200:
        abort(status)
    document, headers = lda.convert_to_requested_format(document, headers, request.environ)
    return document, status, headers

@app.route('/td/items/<i>', methods=['DELETE'])
def delete_item(i):
    document, status, headers = lda.delete_document(request.environ)
    return "", status, headers

@app.route('/td/items/<i>', methods=['PATCH'])
def change_item(i):
    #TODO: add validation
    document, status, headers = lda.patch_document(request.environ, request.json)
    if status != 200:
        abort(status)
    document, headers = lda.convert_to_requested_format(document, headers, request.environ)
    return document, status, headers

@app.route('/td', methods=['DELETE'])
def delete_all():
    document, status, headers = lda.delete_document(request.environ)
    return "", status, headers
