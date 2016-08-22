#!/usr/bin/env bash

set -e
VIRTUAL_ENV_PATH=~/.virtualenvs/dsd/bin/activate

function main {
  source ${VIRTUAL_ENV_PATH}
  case "$1" in
    "ut" )
      run_unit_test;;

    "ft" )
      run_functional_test;;

    "rs" )
      run_server;;

    "sc" )
      start_celery;;
  esac
}

function run_unit_test {
  python manage.py test -v 2 --noinput
}

function run_functional_test {
  echo 'functional tests'
}

function run_server {
  python manage.py runserver
}

function start_celery {
    if [ "$1" = "prod" ]; then
        export DJANGO_SETTINGS_MODULE="chai.settings_prod"
    else
        export DJANGO_SETTINGS_MODULE="chai.settings_dev"
    fi
    celery worker -A chai -B --loglevel=INFO
}


main $@
exit 0
