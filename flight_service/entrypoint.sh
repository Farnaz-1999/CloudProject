#!/bin/sh

python3 manage.py migrate
python3 load_data.py
python3 manage.py runserver 0.0.0.0:9001
