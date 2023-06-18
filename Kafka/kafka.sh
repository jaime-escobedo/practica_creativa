#!/bin/bash
cd /kafka_2.12-3.0.0

echo ----------------Iniciando kafka-------------- 

bin/kafka-server-start.sh config/server.properties --override listeners=${KAFKA_LISTENERS} --override advertised.listeners=${KAFKA_ADVERTISED_LISTENERS} --override zookeeper.connect=${KAFKA_ZOOKEEPER_CONNECT}
