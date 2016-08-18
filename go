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

main $@
exit 0
