#!/bin/bash


echo "setup db"
source ~/.virtualenvs/dsd/bin/activate
python manage.py migrate
python manage.py loaddata dsd/fixtures/attributes.json
python manage.py loaddata dsd/fixtures/dataElement.json


echo "run cron job"
python manage.py crontab add