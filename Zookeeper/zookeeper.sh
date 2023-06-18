#!/bin/bash
cd /kafka_2.12-3.0.0

echo ----------------Iniciando zookeeper-------------- 

bin/zookeeper-server-start.sh config/zookeeper.properties
