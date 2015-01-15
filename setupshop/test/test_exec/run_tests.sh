#!/bin/bash

#TODO: set location to lda-examples root via ~

# start setupshop server and direct output to log file
cd setupshop
nohup sh run.sh > ~/setupshop_server_test.log &

# start siteserver and direct output to log file
cd ../../lda-siteserver
nohup sh run.sh > ~/site_server_test.log &

# wait for servers to come up
sleep 10

# create test data for setupshop
cd test;
sh test_data_create.sh;

# create test data for siteserver
cd ../../lda-examples/setupshop/test;
sh setupshop_test_data_create.sh;

# execute tests
cd test_exec;
py.test

# TODO: kill servers

# output siteserver log
cd ../..
cat ~/site_server_test.log

# output setupshot log
cd ../../lda-examples
cat ~/setupshop_server_test.log

