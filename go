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

    "rdb" )
      reset_db;;
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

function reset_db {
  if [ "$1" = "test" ]; then
    echo "+++ Resetting test database dsd_test..."
    echo "drop database dsd_test; create database dsd_test;" | psql -h localhost -U postgres
    python manage.py makemigrations --settings=dsd.test_settings
    python manage.py migrate --settings=dsd.test_settings
  else
    echo "+++ Resetting database dsd..."
    echo "drop database dsd; create database dsd;" | psql -h localhost -U postgres
    python manage.py makemigrations
    python manage.py migrate
  fi
}

main $@
exit 0
