#!/bin/bash
ls venv-ehr/bin
source "./venv-ehr/bin/activate"
export DEV_DATABASE_URL="mysq://root:password@localhost/ehr"
export MAIL_USERNAME="healthhubnotify@gmail.com"
export MAIL_PASSWORD="healthandwellness1"
ln -s /Applications/MAMP/tmp/mysql/mysql.sock /tmp/mysql.sock
open -a Terminal "`python3 manage.py runserver`"
#redis-server
#rq worker forum-tasks
#celery worker -A celery_worker.celery --loglevel=info
#celery beat -A celery_workecelery --loglevel=info

