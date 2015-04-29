Writing a LDA servers using simple JSON and Flask
=================================================

Although The ld4apps framework (http://ld4apps.github.io/) uses RDF for its internal data model, it also supports a simple
application/json user format that is very desirable for many client applications (especially UIs) and can also be used to write
an application server. Using LDA with this simple JSON format provides all the advantages of using the LDA framework, including
easy integration with other RDF-based applications, only with much less need to understand the details of the framework or even RDF itself.

Writing LDA servers using simple JSON is done using an server implementation library in the lda.py module of lda-serverlib.
Using lda.py has the added advantage that it can be used in conjunction with other popular python WSGI application frameworks
like Flask (http://flask.pocoo.org/) for example. When using lda.py, the user's application is in control of the WSGI application
and simply calls library functions in lda.py to leverage ld4apps functionality. This is very different from the other supported approach
where LDA provides a fully functioning WSGI application server (logic_server.py) which delegates to a Domain_logic implementation class
(usually example_logic_tier.py, which implements a fully functional generic CRUD application for RDF resources), and the framework
user simply provides a subclass to override appropriate methods to add application specific behavior. 

An application written using the 'lda.py' library is much simpler to understand, both because it uses simple JSON for its client
data model and, because it works with popular python frameworks, there are much fewer LDA details that needs to be understood
when implementing a server.

```
{
  "_subject": "http://example.localhost:3007/td/items/10.1",
  "rdf_type": "http://example.org/todo#Item",
  "dc_title": "do the first thing - today!",
  "ce_item_of": "http://example.localhost:3007/td/items",
  "ac_resource-group": "http://example.localhost:3007/",
  "ce_owner": "http://example.localhost:3007/unknown_user/bbe9b9c5-af2c-44bf-8489-9952b0c1b7a8",
  "dc_creator": "http://example.localhost:3007/unknown_user/bbe9b9c5-af2c-44bf-8489-9952b0c1b7a8",
  "dc_created": "2015-04-17T20:46:26.749000+00:00",
  "ce_lastModifiedBy": "http://example.localhost:3007/unknown_user/03defb60-9689-4e64-a8a8-c79adc7426f2",
  "ce_lastModified": "2015-04-17T20:46:26.781000+00:00",
  "ce_revision": "1",
  "ce_history": ["http://example.localhost:3007/td_history/11.1"]
}
```
