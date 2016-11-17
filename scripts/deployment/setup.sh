#!/bin/bash


echo "setup db"
sleep 10

source ~/.virtualenvs/dsd/bin/activate
python manage.py migrate
python manage.py loaddata dsd/fixtures/attributes.json
python manage.py loaddata dsd/fixtures/category_options.json
python manage.py loaddata dsd/fixtures/categories.json
python manage.py loaddata dsd/fixtures/category_combinations.json
python manage.py loaddata dsd/fixtures/data_elements.json
python manage.py loaddata dsd/fixtures/coc_relations.json
python manage.py loaddata dsd/fixtures/historical_coc_relations.json
python manage.py createcachetable dsd_cache

echo "post organisation units and attributes to dhis2"
while true; do
    sleep 1
    if curl --fail dhis2:8080; then
        echo "posting."
        python manage.py shell_plus --plain < dsd/deployment/metadata_service.py
        break
    fi;
done

echo "run cron job"
python manage.py crontab add