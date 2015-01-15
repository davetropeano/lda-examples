#!/bin/bash

#set location to lda-examples/todo
cd ../..

# start setupshop server and direct output to log file
nohup sh run.sh > ~/todo_server_test.log &

# wait for servers to come up
sleep 10

# execute tests
cd test/test_exec;
pytest_result=py.test

# TODO: kill servers

# output server log
echo ''
echo '================== todo_server_test.log ======================================'
cat ~/todo_server_test.log

# return py.test result
exit ${pytest_result}