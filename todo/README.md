Todo Sample
-----------

This is an example of an LDA-based 'todo list' application.

**This application requires a running mongodb database server.**
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
