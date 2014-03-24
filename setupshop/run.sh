#!/bin/sh
export PYTHONPATH=.:./src:./libs/MongoDBStorage:./libs/LogicLibrary;
python test/test_server.py