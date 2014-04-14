#!/bin/sh
set PYTHONPATH=./src:../../lda-serverlib/mongodbstorage:../../lda-serverlib/logiclibrary:$PYTHONPATH
python test/test_server.py
