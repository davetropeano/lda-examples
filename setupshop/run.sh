#!/bin/sh
export PYTHONPATH=.:./src:./libs/MongoDBStorage:./libs/LogicLibrary:$PYTHONPATH
python test/test_server.py
