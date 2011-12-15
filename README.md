
SETUP
======

install python dependncies
-----
* sudo easy_install flask
* sudo easy_install pymongo

mongod
-----
* download mongod 2.1.0+ (or 2.1 nightly)
* start mongod

start web app
-----
* python www.py

run curl
-----
* streaming api docs: https://dev.twitter.com/docs/streaming-api
* sample: curl https://stream.twitter.com/1/statuses/sample.json -u<USERNAME>:<PASSWORD> | mongoimport -d test -c live

all set
-----
[http://127.0.0.1:5000](http://127.0.0.1:5000/)
