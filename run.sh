#! /bin/bash

chmod +x Server/mongo/mongo.sh Server/redis/redis.sh

./Server/mongo/mongo.sh &
./Server/redis/redis.sh &

python3 ./Client/app.py

wait