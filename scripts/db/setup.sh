#!/bin/bash
echo "migrate db"

source ~/.virtualenvs/dsd/bin/activate
python manage.py migrate