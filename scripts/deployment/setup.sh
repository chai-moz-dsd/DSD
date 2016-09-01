#!/bin/bash


echo "setup db"
source ~/.virtualenvs/dsd/bin/activate
python manage.py migrate
python manage.py loaddata dsd/fixtures/attributes.json
python manage.py loaddata dsd/fixtures/dataElement.json

echo "post organisation units and attributes to dhis2"
while true; do
    sleep 1
    if curl --fail dhis2:8080; then
        echo "posting."
        python manage.py shell_plus < dsd.services.post_organ_and_attrs.py
        break
    fi;
done


echo "run cron job"
python manage.py crontab add