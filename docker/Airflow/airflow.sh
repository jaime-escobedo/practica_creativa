#!/bin/bash
airflow users create \
    --username admin \
    --firstname Jack \
    --lastname  Sparrow\
    --role Admin \
    --email example@mail.org \
    --password pass
airflow webserver --port 9090 &
airflow scheduler &
sleep infinity
