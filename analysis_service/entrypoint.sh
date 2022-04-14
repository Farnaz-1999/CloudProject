#!/bin/sh

python3 manage.py inspectdb --database=flight_db > analysis/replica_models.py
python3 manage.py runserver 0.0.0.0:8000
