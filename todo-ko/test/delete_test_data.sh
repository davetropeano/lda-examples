#!/bin/sh
export PYTHONPATH=.:../src:../../../lda-clientlib/python:../../../lda-clientlib/python/test:%PYTHONPATH
python delete_test_data.py
