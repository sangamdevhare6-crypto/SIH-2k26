# VARSHA KRITRIMA BUDHHIH — Django Integrated Login

This version keeps the existing HTML/CSS UI and replaces browser `localStorage` authentication with a Django backend and SQLite database.

## Run on Windows

```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Open: http://127.0.0.1:8000/

Django Admin panel: http://127.0.0.1:8000/admin/

Use the superuser created with `py manage.py createsuperuser` to sign in to the Django Admin panel. The admin panel is the real Django administration interface and is separate from the custom VARSHA dashboard.

## What changed
- Django custom User model
- Passwords stored using Django password hashing
- Session-based login/logout
- Citizen/Admin roles
- Django database (SQLite for easy local setup)
- Signup, login, logout, password reset and current-user API endpoints
- Existing frontend pages retained

For production, use PostgreSQL, HTTPS, environment-based secrets, email-verified password reset, rate limiting, and stricter administrator provisioning.
