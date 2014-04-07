Setupshop Sample
----------------

This example demonstrates a multi-tenant hoster managing a hosted site called 'CloudSupplements' - an online store of vitamins
and health products. Setupshop can be run in different configurations, but here we document what you need to do to run it in a
local development configuration.

This application uses services provided by the [lda-siteserver](https://github.com/ld4apps/lda-siteserver) component of LDA.

**Before attempting to run this example, the siteserver application, mongodb and nginx servers must also be running.**
Instructions for starting them can be found [here](https://github.com/ld4apps/lda-siteserver/blob/master/README.md).

To run the Setupshop application proceed as follows:

1. If you haven't already done so, start the siteserver, mongodb and nginx servers:

   Follow the [siteserver startup instructions](https://github.com/ld4apps/lda-siteserver/blob/master/README.md).  

2. Make sure you have the following line in your /etc/hosts (C:\Windows\System32\Drivers\etc\hosts on Windows) file:

        127.0.0.1 cloudsupplements.localhost

3. cd into the setupshop directory:

        cd lda-examples/setupshop

4. Get the python libraries you need (only needs to be run once):

        python setup.py install

5. Run the setupshop server:

        ./run.sh (or equivalent for your OS)

   You should see the message "test setupshop initiated on host: localhost port: 3006".

6. Create the test data:

        cd test
        ./setupshop_test_data_create.sh

   If successful, you should see a number of POST messages on the console that look something like this:

        ######## POSTed resource: http://localhost:3001/ac/13.1, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/ac/13.2, status: 201
        ######## POSTed resource: http://localhost:3001/ac/13.3, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/ac/13.4, status: 201
        ######## POSTed resource: http://localhost:3001/mt/13.5, status: 201
        ######## POSTed resource: http://localhost:3001/mt/13.6, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.2, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.3, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.4, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.5, status: 201
        ######## POSTed resource: http://localhost:3001/mt/cloudsupplements, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.6, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.7, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.8, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.9, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.10, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.11, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.12, status: 201
        ...
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.60, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.61, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.62, status: 201
        ######## POSTed resource: http://cloudsupplements.localhost:3001/cat/12.63, status: 201
        Done.

At this point, you can point your browser at http://localhost:3001/ where you will initially see no existing sites. 

If you log in as **admin/admin**, the cloudsupplements site will appear. 
You can explore the cloudsupplements site and you can link from there to the store at http://cloudsupplements.localhost:3001/. 
You can also create new sites and you can add new improvements (instances of capabilities) to them. Your choice of capabilities
is currently limited to shop and blog so your improvements need to be of those types. You can create a new shop, but there is
not enough implemented yet to let you completely define your catalog, prices, taxes etc., through the UI. Blogging is even
more embryonic.

You can also create a new account (register) and log in. You use the same account to create new sites that you use to shop at
an existing site - accounts are not specific to a particular capability.
