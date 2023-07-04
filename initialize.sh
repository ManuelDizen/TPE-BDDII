#!/bin/bash

# Creo venv
python3 -m venv venv
source venv/bin/activate

pip install --no-cache-dir -r requirements.txt

docker pull postgres
mkdir -p ~/docker/volumes/postgres
sudo docker run --name tpebdd2 -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres

docker pull couchdb
docker run -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=tpebdd2 -d --name tpebdd2-couch couchdb