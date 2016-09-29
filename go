#!/usr/bin/env bash

set -e
VIRTUAL_ENV_PATH=~/.virtualenvs/dsd/bin/activate

function main {
  source ${VIRTUAL_ENV_PATH}
  case "$1" in
    "ut" )
      if [ "$2" = "--prod" ]; then
        run_unit_test --prod
      elif [ "$2" = "--ci" ]; then
        run_unit_test --ci
      else
        run_unit_test
      fi;;
    "ft" )
      run_functional_test;;

    "seed" )
      seed;;

    "rs" )
      if [ "$2" = "--prod" ]; then
        run_server --prod
      elif [ "$2" = "--ci" ]; then
        run_server --ci
      else
        run_server
      fi;;
    "sh" )
      run_shell;;
    "schedule")
      schedule;;

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
    python manage.py test -v 2 --noinput --settings=chai.settings_test
  fi

}

function run_functional_test {
  echo 'functional tests'
}

function run_server {
  if [ "$1" = "--prod" ]; then
    python manage.py crontab add --settings=chai.settings_prod
    python manage.py createcachetable --settings=chai.settings_prod dsd_cache
    python manage.py runserver --settings=chai.settings_prod
  elif [ "$1" = "--ci" ]; then
    python manage.py crontab add --settings=chai.settings_ci
    python manage.py createcachetable --settings=chai.settings_ci dsd_cache
    python manage.py runserver --settings=chai.settings_ci
  else
    python manage.py crontab add --settings=chai.settings_dev
    python manage.py createcachetable --settings=chai.settings_dev dsd_cache
    python manage.py runserver --settings=chai.settings_dev
  fi
}

function schedule {
    python manage.py crontab add --settings=chai.settings_dev
}

function run_shell {
  python manage.py shell_plus --settings=chai.settings_dev
}
function reset_db {
  if [ "$1" = "test" ]; then
    echo "+++ Resetting test database dsd_test..."
    echo "drop database dsd_test; create database dsd_test;" | psql -h localhost -U postgres
    python manage.py makemigrations --settings=chai.settings_test
    python manage.py migrate --settings=chai.settings_test
  else
    echo "+++ Stop sessions to dsd..."
    echo "select pg_terminate_backend(pid) from pg_stat_activity where datname='dsd';" | psql -h localhost -U postgres
    echo "+++ Resetting database dsd..."
    echo "drop database dsd; create database dsd;" | psql -h localhost -U postgres
    python manage.py makemigrations --settings=chai.settings_dev
    python manage.py migrate --settings=chai.settings_dev
  fi
}

function seed {
    python manage.py loaddata dsd/fixtures/attributes.json --settings=chai.settings_dev
    python manage.py loaddata dsd/fixtures/category_options.json --settings=chai.settings_dev
    python manage.py loaddata dsd/fixtures/categories.json --settings=chai.settings_dev
    python manage.py loaddata dsd/fixtures/category_combinations.json --settings=chai.settings_dev
    python manage.py loaddata dsd/fixtures/data_elements.json --settings=chai.settings_dev
    python manage.py loaddata dsd/fixtures/coc_relations.json --settings=chai.settings_dev
    python manage.py createcachetable --settings=chai.settings_dev dsd_cache
}

main $@
exit 0