#!/bin/bash

# Creo venv
python3 -m venv venv
source venv/bin/activate

pip install --no-cache-dir -r requirements.txt

docker pull postgres
mkdir -p ~/docker/volumes/postgres
sudo docker run --name tpebdd2 -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres