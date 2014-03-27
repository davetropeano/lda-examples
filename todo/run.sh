#!/bin/sh
export PYTHONPATH=./src:../../lda-serverlib/mongodbstorage:../../lda-serverlib/logiclibrary
python test/test_server.py
