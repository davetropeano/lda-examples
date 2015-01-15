#!/bin/bash

#TODO: set location to lda-examples root via ~
cd ~
pwd

# start setupshop server and direct output to log file
cd todo
nohup sh run.sh > ~/todo_server_test.log &

# wait for servers to come up
sleep 10

# execute tests
cd ../../lda-examples/todo/test/test_exec;
py.test

# TODO: kill servers

# output server log
cd ../..
echo ''
echo '================== todo_server_test.log ======================================'
cat ~/todo_server_test.log
