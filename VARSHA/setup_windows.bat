@echo off
cd /d "%~dp0backend"
py -m venv venv
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
