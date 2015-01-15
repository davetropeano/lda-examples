#!/bin/bash

#set location to lda-examples/setupshop
cd ../..

# start setupshop server and direct output to log file
nohup sh run.sh > ~/setupshop_server_test.log &

# start siteserver and direct output to log file
cd ../../lda-siteserver
nohup sh run.sh > ~/site_server_test.log &

# wait for servers to come up
sleep 10

# create test data for setupshop
cd test
sh test_data_create.sh

# create test data for siteserver
cd ../../lda-examples/setupshop/test
sh setupshop_test_data_create.sh

# execute tests
cd test_exec
pytest_result=py.test

# TODO: kill servers

# output siteserver log
echo ''
echo '================== todo_server_test.log ======================================'
cat ~/site_server_test.log

# output setupshot log
echo ''
echo '================== todo_server_test.log ======================================'
cat ~/setupshop_server_test.log

# return py.test result
exit ${pytest_result}