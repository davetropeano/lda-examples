lda-examples
============

This project contains several examples &amp; tutorials for Linked Data for Applications (LDA).

Note: if you don't have python 2.7, you need to install it before proceeding.

Before attempting to run any of the examples, if you haven't already done so, 
bring up a virtual machine with Nginx and MongoDB in it:
```sh
    vagrant up
```
The first time you do this it might take minute or two. Subsequent times should be around 15 seconds.

cd into todo directory
```sh
    cd todo
```
   
Get the python libraries you need (only needs to be done once)
```sh
    python setup.py install
```
    
Run the todo server
```sh
    cd test
    ./run.sh (or equivalent for your OS)
```
    
You should see the message "todo initiated on host: localhost port: 3007"
