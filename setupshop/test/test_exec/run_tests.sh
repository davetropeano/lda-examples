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

# create test data for siteserver
cd test
echo 'travis_fold:start:siteserver_testdata'
echo 'siteserver_testdata create'
sh test_data_create.sh
echo 'travis_fold:end:siteserver_testdata'

# create test data for setupshop
cd ../../lda-examples/setupshop/test
echo 'travis_fold:start:setupshop_testdata'
echo 'setupshop_testdata create'
sh setupshop_test_data_create.sh
echo 'travis_fold:end:setupshop_testdata'

# execute tests
cd test_exec
py.test
pytest_result=$?

# TODO: kill servers

# output siteserver log
echo 'travis_fold:start:site_server_test.log'
echo 'site_server_test output'
cat ~/site_server_test.log
echo 'travis_fold:end:site_server_test.log'

# output setupshot log
echo 'travis_fold:start:setupshop_server_test.log'
echo 'setupshop_server_test output'
cat ~/setupshop_server_test.log
echo 'travis_fold:end:setupshop_server_test.log'

# return py.test result
exit ${pytest_result}