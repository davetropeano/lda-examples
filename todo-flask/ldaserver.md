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

For example, the "mysys" system (SystemDeployment) that is created in the helloworld sample 
(https://github.rtp.raleigh.ibm.com/frankb-ca/deployexamples/tree/master/helloworld) looks like this in Turtle:

Turtle RDF representation of the "mysys" system
-----------------------------------------------
```
@prefix ns1: <http://purl.org/dc/terms/> .
@prefix ns2: <http://ibm.com/ce/ns#> .
@prefix ns3: <http://ibm.com/ce/ac/ns#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.localhost:3303/ft/features/27.2> a ns2:FTFeature ;
rdfs:label "feature2" ;
ns3:resource-group <http://example.localhost:3303/> ;
ns2:enabled true ;
ns2:feature_of <http://example.localhost:3303/ft/features> ;
ns2:lastModified "2015-04-16T22:03:41.132000+00:00" ;
ns2:lastModifiedBy <http://example.localhost:3303/unknown_user/4996f791-61d5-4965-bba2-01420982db4d> ;
ns2:owner <http://example.localhost:3303/unknown_user/4996f791-61d5-4965-bba2-01420982db4d> ;
ns2:revision "0" ;
ns1:created "2015-04-16T22:03:41.132000+00:00" ;
ns1:creator <http://example.localhost:3303/unknown_user/4996f791-61d5-4965-bba2-01420982db4d> ;
ns1:description "description of feature #2" .
```

Turtle is one of several standard RDF representations supported by the framework, however, the format
that we use internally for programming in Python and JavaScript is a simplified RDF/JSON-like representation
that looks like this:

RDF/JSON-like in-memory representation of the "mysys" system
------------------------------------------------------------
```javascript
{
  "http://example.localhost:5101/sy/mysys": {
    "http://ibm.com/ce/ns#lastModified": Date(2014-12-08T17:57:34.068Z),
    "http://ibm.com/ce/ns#system_deployment_public_domain_name": "localhost:6002",
    "http://ibm.com/ce/ns#in_region": URI(http://example.localhost:5101/sy/region),
    "http://ibm.com/ce/ns#transitions": URI(http://example.localhost:5101/xdo/system_transitions?http%3A//example.localhost%3A5101/sy/mysys),
    "http://ibm.com/ce/ns#microservice_registry_service_implementations": [
      URI(http://example.localhost:5101/sx/service_implementations?http%3A//example.localhost%3A5101/sy/mysys),
      URI(http://example.localhost:5101/sx/service_implementations?http%3A//example.localhost%3A5101/sy/mysys)
    ],
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": URI(http://ibm.com/ce/ns#SystemDeployment),
    "http://www.w3.org/2000/01/rdf-schema#label": "mysys",
    "http://purl.org/dc/terms/created": Date(2014-12-08T17:57:28.501Z),
    "http://ibm.com/ce/ns#lastModifiedBy": URI(http://example.localhost:5101/account/fb#owner),
    "http://ibm.com/ce/ns#microservice_registry_ips": "172.17.42.100 172.17.42.101",
    "http://ibm.com/ce/ns#owner": URI(http://example.localhost:5101/account/fb#owner),
    "http://ibm.com/ce/ns#microservice_registry_services": [
      URI(http://example.localhost:5101/sx/services?http%3A//example.localhost%3A5101/sy/mysys),
      URI(http://example.localhost:5101/sx/services?http%3A//example.localhost%3A5101/sy/mysys)
    ],
    "http://ibm.com/ce/ns#history": [
      URI(http://example.localhost:5101/sy_history/2.13)
    ],
    "http://ibm.com/ce/ac/ns#resource-group": URI(http://example.localhost:5101/),
    "http://ibm.com/ce/ns#application_deployments": URI(http://example.localhost:5101/sy/mysys/application_deployments),
    "http://purl.org/dc/terms/creator": URI(http://example.localhost:5101/account/fb#owner),
    "http://ibm.com/ce/ns#active_version_deployments": URI(http://example.localhost:5101/sy/mysys/active_version_deployments),
    "http://ibm.com/ce/ns#servicex": URI(http://example.localhost:5101/sx/root?http%3A//example.localhost%3A5101/sy/mysys),
    "http://ibm.com/ce/ns#system_elb": URI(http://example.localhost:5101/iaas/elbs/example_elb_mysys),
    "http://ibm.com/ce/ns#state": "System_started",
    "http://ibm.com/ce/ns#modificationCount": 1,
    "http://ibm.com/ce/ns#allVersions": URI(http://example.localhost:5101/sy/mysys/allVersions)
  }
}
```

We find this format very convenient for working in languages with built-in JSON support (Note: we also have an even
simpler variant of this which we call "simple json" that we use for UI programming in JavaScript).

For persistent storage in NoSQL databases, however, we found that a more JSON-LD like format is better. For example, in MongoDB "mysys"
looks like this:

MongoDB (JSON-LD inspired) persistent representation of the "feature2" Feature
------------------------------------------------------------------------------
```javascript
> db['example/ft'].find({"_id": "features/27.2"}).pretty()
{
  "_id" : "features/27.2",
  "_createdBy" : "urn:ce:/unknown_user/4996f791-61d5-4965-bba2-01420982db4d",
  "@graph" : [
    {
      "http://ibm%2Ecom/ce/ns#enabled" : true,
      "http://ibm%2Ecom/ce/ac/ns#resource-group" : {
        "type" : "uri",
        "value" : "urn:ce:/"
      },
      "http://ibm%2Ecom/ce/ns#owner" : {
        "type" : "uri",
        "value" : "urn:ce:/unknown_user/4996f791-61d5-4965-bba2-01420982db4d"
      },
      "http://www%2Ew3%2Eorg/2000/01/rdf-schema#label" : "feature2",
      "http://purl%2Eorg/dc/terms/description" : "description of feature #2",
      "http://www%2Ew3%2Eorg/1999/02/22-rdf-syntax-ns#type" : {
        "type" : "uri",
        "value" : "http://ibm.com/ce/ns#FTFeature"
      },
      "http://ibm%2Ecom/ce/ns#feature_of" : {
        "type" : "uri",
        "value" : "urn:ce:/ft/features"
      },
      "@id" : "urn:ce:/ft/features/27.2"
    }
    ],
    "_modificationCount" : 0,
    "_lastModifiedBy" : "urn:ce:/unknown_user/4996f791-61d5-4965-bba2-01420982db4d",
    "_lastModified" : ISODate("2015-04-16T22:03:41.132Z"),
    "_created" : ISODate("2015-04-16T22:03:41.132Z"),
    "@id" : "urn:ce:/ft/features/27.2"
}
```

Notice the fundamental difference is that the subject of the triples is not a key but rather the value of an @id property.
This is very important when querying the resources. Two other notable points:

1. URLs have been made relative (e.g., we changed http://example.localhost:5101/sy/mysys to urn:ce:/sy/mysys) so that
   the data can be moved to a different server without conversion
2. Some of the triples in the RDF are not stored persistently. They are instead manufactured by the framework from queries

A simple example of a manufactured property is "http://ibm.com/ce/ns#application_deployments" which is the collection
of ApplicationDeployment resources, i.e., the applications of the system. Continuing with the helloworld example, we
have an application named "myapp" that is in the "mysys" system. The MongoDB representation of "myapp" is as follows:

MongoDB persistent representation of the "myapp" ApplicationDeployment
----------------------------------------------------------------------
```javascript
{
  "_id" : "myapp",
  "_createdBy" : "urn:ce:/account/fb#owner",
  "@graph" : [
    {
      "http://ibm%2Ecom/ce/ns#system_deployment" : {
        "type" : "uri",
        "value" : "urn:ce:/sy/mysys"
      },
      "http://ibm%2Ecom/ce/ns#edgeserver" : true,
      "http://ibm%2Ecom/ce/ac/ns#resource-group" : {
        "type" : "uri",
        "value" : "urn:ce:/"
      },
      "http://ibm%2Ecom/ce/ns#owner" : {
        "type" : "uri",
        "value" : "urn:ce:/account/fb#owner"
      },
      "http://ibm%2Ecom/ce/ns#emergency_contact" : {
        "type" : "uri",
        "value" : "urn:ce:/sy/nally@us.ibm.com"
      },
      "http://www%2Ew3%2Eorg/2000/01/rdf-schema#label" : "myapp",
      "http://www%2Ew3%2Eorg/1999/02/22-rdf-syntax-ns#type" : {
        "type" : "uri",
        "value" : "http://ibm.com/ce/ns#ApplicationDeployment"
      },
      "@id" : "urn:ce:/sy/myapp"
    }
  ],
  "_modificationCount" : 0,
  "_lastModifiedBy" : "urn:ce:/account/fb#owner",
  "_lastModified" : ISODate("2014-12-04T19:30:45.605Z"),
  "_created" : ISODate("2014-12-04T19:30:45.605Z"),
  "@id" : "urn:ce:/sy/myapp"
}
```

Notice that the representation of the application DOES have a property ("http://ibm%2Ecom/ce/ns#system_deployment") pointing
to the system ("mysys") that it is part of. This property is used by the framework to query the system to produce the system's
"http://ibm.com/ce/ns#application_deployments" collection, from above. The client-side query (in this case, the framework is the client)
looks like this:

Query for all ApplicationDeployments in a SystemDeployment
----------------------------------------------------------
```javascript
{
  "_any": {
    "http://ibm.com/ce/ns#system_deployment": URI(http://example.localhost:5101/sy/mysys)
  }
}
```

This "portable" client-side query is converted to an implementation-specific database query. For MongoDB it is converted to the following:

```javascript
{
  "@graph": {
    "$elemMatch": {
      "http://ibm%2Ecom/ce/ns#system_deployment": {"type": "uri", "value": "urn:ce:/sy/mysys"}
    }
  }
}
```

As you can see, we use the $elemMatch query feature of MongoDB for this.

A similer, but slightly more complicated, query is used to generate the "http://ibm.com/ce/ns#active_version_deployments" property 
of the SystemDeployment. This property is defined to be all the version deployments in the system that are in active states (where state is
another property of a version). For example the representation of the "myapp_v1" deployment looks like this:

MongoDB persistent representation of the "myapp" VersionDeployment
------------------------------------------------------------------
```javascript
{
  "@graph" : [
    {
      "@id" : "urn:ce:/sy/myapp_v1",
      "http://ibm%2Ecom/ce/ac/ns#resource-group" : {
        "type" : "uri",
        "value" : "urn:ce:/"
      },
      "http://ibm%2Ecom/ce/ns#active_in" : {
        "type" : "uri",
        "value" : "urn:ce:/sy/mysys"
      },
      "http://ibm%2Ecom/ce/ns#application_deployment" : {
        "type" : "uri",
        "value" : "urn:ce:/sy/myapp"
      },
      "http://ibm%2Ecom/ce/ns#asg" : {
        "type" : "uri",
        "value" : "urn:ce:/iaas/2.5"
      },
      "http://ibm%2Ecom/ce/ns#emergency_contact" : {
        "type" : "uri",
        "value" : "urn:ce:/sy/nally@us.ibm.com"
      },
      "http://ibm%2Ecom/ce/ns#image" : "xdevops/hello",
      "http://ibm%2Ecom/ce/ns#loadbalancer_rule" : "default",
      "http://ibm%2Ecom/ce/ns#owner" : {
        "type" : "uri",
        "value" : "urn:ce:/account/fb#owner"
      },
      "http://ibm%2Ecom/ce/ns#state" : "In_production",
      "http://www%2Ew3%2Eorg/1999/02/22-rdf-syntax-ns#type" : {
        "type" : "uri",
        "value" : "http://ibm.com/ce/ns#VersionDeployment"
      },
      "http://www%2Ew3%2Eorg/2000/01/rdf-schema#label" : "myapp_v1"
    }
  ],
  "@id" : "urn:ce:/sy/myapp_v1",
  "_created" : ISODate("2014-12-04T19:31:05.190Z"),
  "_createdBy" : "urn:ce:/account/fb#owner",
  "_history" : [
    "http://example.localhost:5101/sy_history/2.19",
    "http://example.localhost:5101/sy_history/2.20"
  ],
  "_id" : "myapp_v1",
  "_lastModified" : ISODate("2014-12-04T21:24:14.344Z"),
  "_lastModifiedBy" : "http://example.localhost:5101/unknown_user/01e7f152-3ee8-4521-85b4-6faeecd0cd2b",
  "_modificationCount" : 2
}
```

The generated framework query for the contents of the "http://ibm.com/ce/ns#active_version_deployments" collection looks like this:

Query for active VersionDeployments in a SystemDeployment
---------------------------------------------------------
```javascript
{
  "_any": {
    "http://ibm.com/ce/ns#active_in": URI(http://xdevops.localhost:5101/sy/cloudservices-prod- useast),
    "http://ibm.com/ce/ns#state": {
      "$in": ["Initial", "Instances_started", "Some_traffic_captured", "In_production"]
    }
  }
}
```

The converted MongoDB query looks like this:

```javascript
{
  "@graph": {
    "$elemMatch": {
      "http://ibm%2Ecom/ce/ns#active_in": {"type": "uri", "value": "urn:ce:/sy/mysys"},
      "http://ibm%2Ecom/ce/ns#state": {
        "$in": ["Initial", "Instances_started", "Some_traffic_captured", "In_production"]
      }
    }
  }
}
```

Notice that in addition to the $elemMatch property, this MongoDB query also uses the $in feature to query for a state value
that has one of several values (i.e., the ones considerd to be "active" states).

Sometimes, the RDF triple representing a containment relationship has the container as the subject, instead of the value.
For example, a "Site" resource (used for the multi-tenant support of Proteus) has a triple of the form:
```
   <containing-resource> <http://ibm%2Ecom/ce/ns#sites> <contained-resource>
```
as opposed to the way we modelled the containment relationships for SystemDeployments, e.g.:
```
   <contained-resource> <http://ibm%2Ecom/ce/ns#system_deployment> <containing-resource>
```
In this case, we still store the RDF triple with the contained resource (as opposed to storing it in the containing-resource's
representation) so that it will automatically be deleted when the contained-resource is deleted. Therefore, in this case the
collection contents is still produced using a query. For example, given a Site that looks like this in storage:

MongoDB persistent representation of the "pepsi" tenant Site
------------------------------------------------------------
```javascript
{
  "@graph" : [
    {
      "@id" : "urn:ce:/mt/pepsi",
      "ce_improvements" : [
        "http://pepsi.localhost:5101/sy/mysys"
      ],
      "http://ibm%2Ecom/ce/ac/ns#resource-group" : {
        "type" : "uri",
        "value" : "urn:ce:/mt/pepsi"
      },
      "http://ibm%2Ecom/ce/ns#owner" : {
        "type" : "uri",
        "value" : "urn:ce:/account/fb#owner"
      },
      "http://ibm%2Ecom/ce/ns#site_id" : "pepsi",
      "http://purl%2Eorg/dc/terms/title" : "pepsi",
      "http://www%2Ew3%2Eorg/1999/02/22-rdf-syntax-ns#type" : {
        "type" : "uri",
        "value" : "http://ibm.com/ce/ns#Site"
      }
    },
    {
      "@id" : "urn:ce:/",
      "http://ibm%2Ecom/ce/ns#sites" : {
        "type" : "uri",
        "value" : "urn:ce:/mt/pepsi"
      }
    }
  ],
  "@id" : "urn:ce:/mt/pepsi",
  "_created" : ISODate("2014-12-05T19:35:07.507Z"),
  "_createdBy" : "urn:ce:/account/fb#owner",
  "_history" : [
    "http://hostingsite.localhost:5101/mt_history/2.1"
  ],
  "_id" : "pepsi",
  "_lastModified" : ISODate("2014-12-05T19:36:49.965Z"),
  "_lastModifiedBy" : "http://hostingsite.localhost:5101/account/fb#owner",
  "_modificationCount" : 1
}
```

The query to produce a collection of sites, including the above Site, will look like this:

Query for tenant Sites
----------------------
```javascript
{
  "http://hostingsite.localhost:5101/": {
    "http://ibm.com/ce/ns#sites": "_any"
  }
}
```

The converted MongoDB query looks like this:

```javascript
{
  "@graph": {
    "$elemMatch": {
      "@id": "urn:ce:/",
      "http://ibm%2Ecom/ce/ns#sites": {"$exists": True}
    }
  }
}
```

This query uses another feature of MongoDB, $exists, to check if a property is set to any value.

Collection queries get more complicated when Access Control checking is turned on in the system. In this case, the above query must be
enhanced to only return resources that are accessable by the current user. It achieves this by extending the query with a $and field
to ensure that only accessable resources are returned:

Query for tenant Sites with access control checking
---------------------------------------------------
```javascript
{
  "$and": [
    {
      "@graph": {
        "$elemMatch": {
          "@id": "urn:ce:/",
          "http://ibm%2Ecom/ce/ns#sites": {"$exists": True}
        }
      }
    },
    {
      "@graph": {
        "$elemMatch": {
          "$or": [
            {
              "http://ibm%2Ecom/ce/ns#owner": {"type": "uri", "value": "urn:ce:/account/frankb#owner"}
            },
            {
              "http://ibm%2Ecom/ce/ac/ns#resource-group": {
                "$in": [
                  {"type": "uri", "value": "urn:ce:/"},
                  {"type": "uri", "value": "urn:ce:/mt/sites"},
                  {"type": "uri", "value": "urn:ce:/account"}
                ]
              }
            }
          ]
        }
      }
    }
  ]
}
```

Notice that the accessability check also uses the MondoDB $or field to check for one of 2 $elemMatches (i.e., either
that the current user is the owner of the resource, or the resource is the member of one of the resource-groups to which
the current user has access). This, like all the collection queries, is automatically generated by the framework
from infomation available in the system.


More Query Features
===================

Recall that in the previous section we used the $in query field to search for resources that have a state property with one of several
values in order to produce the active_version_deployments collection:

```javascript
{
  "@graph": {
    "$elemMatch": {
      "http://ibm%2Ecom/ce/ns#active_in": {"type": "uri", "value": "urn:ce:/sy/mysys"},
      "http://ibm%2Ecom/ce/ns#state": {
        "$in": ["Initial", "Instances_started", "Some_traffic_captured", "In_production"]
      }
    }
  }
}
```

The state property, in this example, is a single valued property (i.e., the state of any given version deployment will have exactly one value).
Some properties, however, may be many-valued.


Multi-valued property query
---------------------------

The following resource has two multi-valued properties (colors and urls):

```javascript
{
  "@graph" : [
    {
      "@id" : "urn:ex:/example/1.1",
      "http://example%2Ecom/ex/ns#colors" : [ "red", "green", "blue" ],
      "http://example%2Ecom/ex/ns#urls" : [
        {
          "type" : "uri",
          "value" : "urn:ex:/foo"
        },
        {
          "type" : "uri",
          "value" : "urn:ex:/bar"
        }
      ]
      ...
    }
  ]
}
```

To query for resources that have a multi-valued property with a particular set of values, we use the $all feature of MongoDB as follows:

```javascript
{
  "@graph": {
    "$elemMatch": {
      "http://example%2Ecom/ex/ns#colors": {
        "$all": [ "red", "green", "blue" ]
      }
    }
  }
}
```

This will retrieve resources that have the multi-valued colors property set to all three of the values: "red", "green", and "blue".


Ordered query result
--------------------

Sometimes the order that a set of query results is retuned in, is important. Let's revisit the query for active version deployments
of a system, which we looked at earlier:

```javascript
{
  "@graph": {
    "$elemMatch": {
      "http://ibm%2Ecom/ce/ns#active_in": {"type": "uri", "value": "urn:ce:/sy/mysys"},
      "http://ibm%2Ecom/ce/ns#state": {
        "$in": ["Initial", "Instances_started", "Some_traffic_captured", "In_production"]
      }
    }
  }
}
```

This query will return a set of versions in no particular order. If we wanted to, we can enhance this query to return
the versions in some particular order. For example, to return the versions sorted according to their name/label
(e.g., myapp_v1, myapp_v2, yourapp_v1, etc.) we can enhance the above query as follows:

```javascript
{
  "$query": {
    "@graph": {
      "$elemMatch": {
        "http://ibm%2Ecom/ce/ns#active_in": {"type": "uri", "value": "urn:ce:/sy/mysys"},
        "http://ibm%2Ecom/ce/ns#state": {
          "$in": ["Initial", "Instances_started", "Some_traffic_captured", "In_production"]
        }
      }
    }
  }
  "$orderby": {
    "http://www%2Ew3%2Eorg/2000/01/rdf-schema#label": 1
  }
}
```

As you can see, the $orderby field is used to specify a property to sort on (rdfs:label, in this case). The value of the property
can be 1 or -1, to return the resources in ascending or descending order, respectively.


Modifying Resources
===================

Instead of modifying existing resources using HTTP PUT, we use PATCH with optimistic concurrency control.
A patch request consists of an RDF/JSON document containing the subset of triples that are to be changed, and a mondificationCount
whose value was obtained from an earlier GET request for the resource.

For example, assume we have the "myapp_v1" version of the helloworld example running. If we GET the resource, the current value
would look something like this: 

```javascript
{
  "http://example.localhost:5101/sy/myapp_v1": {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": URI(http://ibm.com/ce/ns#VersionDeployment),
    "http://www.w3.org/2000/01/rdf-schema#label": "myapp_v1",
    "http://ibm.com/ce/ns#image": "xdevops/hello",
    "http://ibm.com/ce/ns#state": "Instances_started",
    "http://ibm.com/ce/ns#asg": URI(http://example.localhost:5101/iaas/2.6),
    ...
    "http://ibm.com/ce/ns#modificationCount": 3
  }
}
```

As you can see, among others, there is an "http://ibm.com/ce/ns#state" property with value "Instances_started" and an
"http://ibm.com/ce/ns#asg" property set to the value of the ASG for the instances. Also notice there is a
"http://ibm.com/ce/ns#modificationCount" property with a current value of 3.

If we now were to stop the instances (e.g., using the XDO UI or SPI), the "myapp_v1" resource would get updated using a patch 
document like this:

RDF/JSON-like patch request to stop the "myapp_v1" version
----------------------------------------------------------
```javascript
{
  "": {
    "http://ibm.com/ce/ns#state": "Initial", 
    "http://ibm.com/ce/ns#asg": null
  }
}
```

Notice that this document only contains the triples that are being changed, i.e., state is being changed to "Initial" and the asg
is being set to null. (Note that setting a property to null actaully means remove the property from the resource.)

To execute the patch, this document, along with an "expected modification count" is passed to the framework. In this case we pass
the value 3, obtained from the previous GET request, above.

The patch request then translates to the following update query in MongoDB:

```javascript
{
  "$set": {
    "_lastModifiedBy": "http://example.localhost:5101/account/fb#owner",
    "@graph.$.http://ibm% 2Ecom/ce/ns#state": "Initial",
    "_lastModified": ISODate("2014-12-05T19:36:49.965Z")
  }, 
  "$unset": {
    "@graph.$.http://ibm%2Ecom/ce/ns#asg": 1
  },
  "$inc": { "_modificationCount": 3},
  "$push": {"_history": "http://example.localhost:5101/sy_history/3.1"}
}
```

Notice that the $set field is used to set the value of the state property to "Initial" and the $unset field is used to remove
the asg property. 

The $inc field will increment the modificationCount from 3 to 4, if its current value is 3. If the modification value does
not match the value in storage (i.e., the resource was updated since the previous GET request when we retrieved the value of 3), 
the patch will fail, and the resource will be left unchanged.

Notice that in addition to the changes requested in the client patch document, the framework also changes
a couple of other properties (_lastModifiedBy and _lastModified) as a side effect of the update request.
The framework also supports undo by maintaining a history list for the reseource. The $push field is used to add another
history document (i.e., resource snapshot) URL to the list of previous snapshots.

The $set and $unset fields are used to update individual properties. Sometimes, however, an update request would like to 
completely remove all RDF triples with a particular subject. To accomplish this in MongoDB, we use the $pull feature like this:

```javascript
{
  "$pull": {
    "@graph": {
      "@id": { "$in": [ "urn:ce:/sy/myapp_v1" ] }
    } 
  },
  "$inc": { "_modificationCount": 4},
  "$push": {"_history": "http://example.localhost:5101/sy_history/3.2"}
}
```

This update request will remove all properties of "myapp_v1", including its corresponding top-level @graph structure in the storage.
Notice that the $in field is also used in this request, allowing more than one subject to be removed at the same time.


MongoDB Storage Implementation
==============================

The MongoDB implementation can be found in https://github.com/ld4apps/lda-serverlib/blob/master/mongodbstorage/operation_primitives.py. 

Each of the Proteus LDA applications that store persistent data (e.g., xdo, servicey, etc.) stores its data in a unique
database. For example, using the "mongo" client command to view the databases in the MongoDB server used for the helloworld
example, we can see the following databases:

```
> show dbs
iaas_docker     0.203125GB
local   0.078125GB
servicey        0.203125GB
siteserver      0.203125GB
xdevops 0.203125GB
```

The interface between the LDA framework and the storage implementation consists of the following functions:

```python
create_document(user, document, public_hostname, tenant, namespace, resource_id=None)
get_document(user, public_hostname, tenant, namespace, documentId)
delete_document(user, public_hostname, tenant, namespace, document_id)
patch_document(user, mod_count, new_values, public_hostname, tenant, namespace, document_id)
execute_query(user, query, public_hostname, tenant, namespace, projection=None)
drop_collection(user, public_hostname, tenant, namespace)
get_prior_versions(user, public_hostname, tenant, namespace, history)
```

Notice that every one of the storage functions includes at least the following parameters:

1. tenant - this is the tenant identifier usually encoded in the domain name protion of a resource URL
   (e.g., 'pepsi' in http://pepsi.localhost:5101/)
2. namespace - the micro-app namespace which is usually the first path segment of a resource URL 
   (e.g., 'sy' in http://pepsi.localhost:5101/sy/mysys)

These two arguments uniquely identify a data collection in which to add, remove, or query. In the MongoDB implementation
this translates to a MongoDB collection named ```<tenant>/<namespace>``` (e.g., pepsi/sy).

The 'sy' micro-app is implemented by servicey, so we can look at the servicey database to see its collections:

```
> use servicey
switched to db servicey
> show collections
example/sy
example/sy_history
lineages_collection
system.indexes
xdevops/sy
xdevops/sy_history
```

Recall that the helloworld example uses tenant 'xdevops' for the Proteus system itself, and 'example' for the helloworld
system. Therefore, among other collections (automatically maintained by the frameowork) we see the two main collections 
'xdevops/sy' and 'example/sy', which contain the system, applications, and deployments corresponding to URLs of the form
```http://xdevops.localhost:5101/sy/<document_id>``` and ```http://example.localhost:5101/sy/<document_id>```, respectively.

For example, we can display the stored SystemDeployment ("mysys") described in the previous section as follows:

```
> db["example/sy"].find({_id:"mysys"}).pretty()
```
```javascript
{
  "@graph" : [
    {
      "@id" : "urn:ce:/sy/mysys",
      "http://ibm%2Ecom/ce/ac/ns#resource-group" : {
        "type" : "uri",
        "value" : "urn:ce:/"
      },
      "http://ibm%2Ecom/ce/ns#in_region" : {
        "type" : "uri",
        "value" : "urn:ce:/sy/region"
      },
      "http://ibm%2Ecom/ce/ns#microservice_registry_ips" : "172.17.42.100 172.17.42.101",
      "http://ibm%2Ecom/ce/ns#owner" : {
        "type" : "uri",
        "value" : "urn:ce:/account/fb#owner"
      },
      "http://ibm%2Ecom/ce/ns#state" : "System_started",
      "http://ibm%2Ecom/ce/ns#system_deployment_public_domain_name" : "localhost:6001",
      "http://ibm%2Ecom/ce/ns#system_elb" : {
        "type" : "uri",
        "value" : "urn:ce:/iaas/elbs/example_elb_mysys"
      },
      "http://www%2Ew3%2Eorg/1999/02/22-rdf-syntax-ns#type" : {
        "type" : "uri",
        "value" : "http://ibm.com/ce/ns#SystemDeployment"
      },
      "http://www%2Ew3%2Eorg/2000/01/rdf-schema#label" : "mysys"
    }
  ],
  "@id" : "urn:ce:/sy/mysys",
  "_created" : ISODate("2014-12-04T19:30:16.026Z"),
  "_createdBy" : "urn:ce:/account/fb#owner",
  "_history" : [
    "http://example.localhost:5101/sy_history/2.18"
  ],
  "_id" : "mysys",
  "_lastModified" : ISODate("2014-12-04T19:30:22.008Z"),
  "_lastModifiedBy" : "http://example.localhost:5101/account/fb#owner",
  "_modificationCount" : 1
}
```


Summary of MongoDB Features Being Used by Proteus
=================================================

To recap, the Proteus/ld4apps framework uses the following MongoDB querry features to generate containers and to support other queries:

1. $elemMatch
2. $in
3. $exists
4. $and
5. $or
6. $all
7. $orderby

Patch requests use the following MongoDB update features:

1. $inc
2. $push
3. $set
4. $unset
5. $pull
