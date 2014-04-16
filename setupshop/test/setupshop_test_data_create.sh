#!/bin/sh
set PYTHONPATH=.:../src:../../../lda-clientlib/python:../../../lda-clientlib/python/test:%PYTHONPATH
python setupshop_test_data_create.py "$1"
