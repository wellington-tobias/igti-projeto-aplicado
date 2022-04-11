#!/bin/bash

# install extra python packages
# sudo python3 -m pip install -U pip
# sudo python3 -m pip install -U setuptools
# sudo python3 -m pip install psycopg2-binary boto3

# # install extra jars
# POSTGRES_JAR="postgresql-42.2.8.jar"
# wget -nv "https://jdbc.postgresql.org/download/${POSTGRES_JAR}"
# sudo chown -R hadoop:hadoop ${POSTGRES_JAR}
# mkdir -p /home/hadoop/extrajars/
# cp ${POSTGRES_JAR} /home/hadoop/extrajars/

sudo yum -y install gcc postgresql-devel
sudo python3 -m pip install -U pip
sudo python3 -m pip install -U setuptools
sudo python3 -m pip install psycopg2