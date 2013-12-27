#!/bin/bash
# Run the webserver, run the tests and kill the webserver!
python server.py &
ID=$!
python freetests.py
kill $ID
#pkill -P $$
