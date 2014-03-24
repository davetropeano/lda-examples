set PYTHONPATH=.;..\src;..\..\..\lda-serverlib\logiclibrary
set SERVICE_HOSTNAME=localhost:3001
python delete_testsite_data.py
python setupshop_test_data_create.py