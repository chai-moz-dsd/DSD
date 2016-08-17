#!/usr/bin/env bash

set -e
VIRTUAL_ENV_PATH=~/.virtualenvs/dsd/bin/activate

function main {
  case "$1" in
    "ut" )
      run_unit_test;;

    "rs" )
      run_server;;

  esac
}

function run_unit_test {
  source ${VIRTUAL_ENV_PATH}
  python manage.py test -v 2 --noinput
}

function run_server {
  source ${VIRTUAL_ENV_PATH}
  python manage.py runserver
}

main $@
exit 0
