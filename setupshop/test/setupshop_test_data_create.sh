#!/bin/sh
export PYTHONPATH=.:../src:../../../lda-serverlib/logiclibrary
python setupshop_test_data_create.py "$1"
