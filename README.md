lda-examples
============

This project contains several examples and tutorials for Linked Data for Applications (LDA).

`Note: if you don't have python 2.7, you need to install it before proceeding.`

If you are new to LDA, you should start by looking at the 'Todo Sample' and its 
corresponding [tutorial](http://ld4apps.github.io/developing-lda-applications/index.html).

Todo Sample
-----------

This is an example of an LDA-based 'todo list' application. **This application requires a running mongodb database server.**
See [Downloading the Software](http://ld4apps.github.io/downloading-the-software/index.html) for instructions.

To run the Todo application proceed as follows:

1. Start a database server, if you haven't already done so:

        cd lda-examples
        vagrant up
        
   or
   
        cd <mongodb-installation-directory>/bin
        mongod
        
2. cd into the todo directory:

        cd lda-examples/todo

3. Get the python libraries you need (only needs to be run once):

        python setup.py install

4. Run the todo server:

        ./run.sh (or equivalent for your OS)

   You should see the message "todo initiated on host: localhost port: 3007".

At this point, you can point your browser at http://localhost:3007/items where you should see a very
simple UI that allows you to add and view items on a todo list. 
For more details, refer to [Developing LDA Applications](http://ld4apps.github.io/developing-lda-applications/index.html).

Setupshop Sample
----------------

This example demonstrates a multi-tenant hoster managing a hosted site called 'CloudSupplements' - an online store of vitamins
and health products. Setupshop can be run in different configurations, but here we document what you need to do to run it in a
local development configuration.

This application uses services provided by the [lda-siteserver](https://github.com/ld4apps/lda-siteserver) component of LDA.
Before attempting to run this example, the siteserver application, mongodb and nginx servers must also running.
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
