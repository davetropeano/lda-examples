#!/bin/sh
export PYTHONPATH=./src:../../lda-clientlib/python:../../lda-serverlib/mongodbstorage:../../lda-serverlib/logiclibrary:$PYTHONPATH
python test/test_server.py
