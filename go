#!/usr/bin/env bash

set -e
VIRTUAL_ENV_PATH=~/.virtualenvs/dsd/bin/activate

function main {
  source ${VIRTUAL_ENV_PATH}
  case "$1" in
    "ut" )
      if [ "$2" = "--prod" ]; then
        run_unit_test --dev
      elif [ "$2" = "--ci" ]; then
        run_unit_test --ci
      else
        run_unit_test
      fi;;
    "ft" )
      run_functional_test;;

    "rs" )
      run_server;;

    "rdb" )
      reset_db;;
  esac
}

function run_unit_test {
  if [ "$1" = "--prod" ]; then
    python manage.py test -v 2 --noinput --settings=chai.settings_prod
  elif [ "$1" = "--ci" ]; then
    python manage.py test -v 2 --noinput --settings=chai.settings_ci
  else
    python manage.py test -v 2 --noinput --settings=chai.settings_dev
  fi

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
    python manage.py makemigrations --settings=chai.settings_test
    python manage.py migrate --settings=chai.settings_test
  else
    echo "+++ Resetting database dsd..."
    echo "drop database dsd; create database dsd;" | psql -h localhost -U postgres
    python manage.py makemigrations --settings=chai.settings_dev
    python manage.py migrate --settings=chai.settings_dev
  fi
}

main $@
exit 0
