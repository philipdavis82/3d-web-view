#!/bin/bash
python3 manage.py migrate
export DJANGO_SUPERUSER_PASSWORD=admin
export DJANGO_SUPERUSER_USERNAME=admin
python3 manage.py createsuperuser --noinput --email admin@admin.admin
python3 manage.py demo
echo ""
echo -e "[\e[1;32mDEMO\e[0m] Demo server started at http://127.0.0.1:8000"
echo -e "[\e[1;32mDEMO\e[0m] Admin loging credentials: username: \e[1;32madmin\e[0m, password: \e[1;32madmin\e[0m"
echo ""
python3 manage.py runserver
