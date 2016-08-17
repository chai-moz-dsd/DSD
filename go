#!/usr/bin/env bash

set -e

function main {
  case "$1" in
    "ut" )
      run_unit_test;;

  esac
}

function run_unit_test {
  source ~/.virtualenvs/dsd/bin/activate
  python manage.py test -v 2 --noinput
}

main $@
exit 0
