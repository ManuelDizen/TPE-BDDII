#!/bin/bash

python3 -m venv venv
source venv/bin/activate

uvicorn main:app --reload

# Para killear los procesos que usen uvicorn: sudo lsof -t -i tcp:8000 | xargs kill -9