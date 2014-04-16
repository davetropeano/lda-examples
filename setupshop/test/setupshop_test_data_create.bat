set PYTHONPATH=.;..\src;..\..\..\lda-clientlib\python;..\..\..\lda-clientlib\python\test
set SERVICE_HOSTNAME=localhost:3001
python delete_testsite_data.py
python setupshop_test_data_create.py