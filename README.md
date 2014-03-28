lda-examples
============

This project contains several examples &amp; tutorials for Linked Data for Applications (LDA).

`
Note: if you don't have python 2.7, you need to install it before proceeding.
`

Before attempting to run any of the examples, if you haven't already done so, 
bring up a virtual machine with Nginx and MongoDB in it:

```sh
vagrant up
```

The first time you do this it might take minute or two. Subsequent times should be around 15 seconds.

Todo Sample
-----------

This is an example of an LDA-based 'todo list' application. To run the application proceed as follows:

1. cd into the todo directory:
```sh
cd lda-examples/todo
```
1. Get the python libraries you need (only needs to be done once):
```sh
python setup.py install
```
1. Run the todo server:
```sh
cd test
./run.sh (or equivalent for your OS)
```
You should see the message "todo initiated on host: localhost port: 3007".

At this point, you can point your browser at http://localhost:3007/items where you should see a very
simple UI that allows you to add and view items on a todo list.

Setupshop Sample
----------------

In this section we will take you through a brief demo of an example system we are in the process of writing. The system is currently deployed on a single virtual machine on SoftLayer. It's URL is http://cloudapps4.me. It runs - at least to some degree - you can try it. CloudApps4.me is a multi-tenant hoster. Currently CloudApps4.me has a single customer whose site is called 'CloudSupplements' - an online store of vitamins and health products. Because our system is still under construction, we wrote scripts to create most of the data for cloudsupplements - you cannot create it all through the UI yet. However, the scripts that created the data use the same public HTTP REST API that the UI will use - we did not exploit any sort of 'backdoor' to create the data. You can go directly to http://clou dsupplements.cloudapps4.me and see the store. You can browse the catalog and fill your cart. You cannot yet check out - don't wait at your mailbox for the mail carrier to arrive. The shopping UI is built using the popular KnockoutJS data-binding framework, which we like quite a bit, but we do not prescribe an approach to UI construction and you can use what you like in your own subsystems.

If you go to http://cloudapps4.me you will initially see no existing sites. If you log in as admin/admin, the cloudsupplements site will appear. You can explore the cloudsupplements site and you can link from there to the store at http://cloudsupplements.cloudapps 4.me. You can also create new sites and you can add new improvements (instances of capabilities) to them. Your choice of capabilities is currently limited to shop and blog so your improvements need to be of those types. You can create a new shop, but - as I said above - there is not enough implemented yet to let you define your catalog, prices, taxes etc. through the UI. Blogging is even more embryonic.

You can also create a new account (register) and log in. You use the same account to create new sites that you use to shop at an existing site - accounts are not specific to a particular capability.
