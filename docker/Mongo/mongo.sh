#!/bin/bash
cd /mongo

mongod --bind_ip_all &

./import_distances.sh

sleep infinity
