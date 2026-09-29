# VARSHA KRITRIMA BUDHHIH — AI Flood Risk Prediction System

> **SIH 2026** — Django + ML powered flood monitoring and alert system with Citizen/Admin roles.

---

## 🖥️ Run Locally (Windows)

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

Use the superuser created with `py manage.py createsuperuser` to sign in to the Django Admin panel.

**Default credentials:**
```
Username: admin
Password: Admin@12345
```

---

## 🚀 Free Deployment — Railway.app (Recommended)

Railway.app is **100% free** for hobby projects. No credit card needed.

### Step 1 — Railway Account Banao

1. [https://railway.app](https://railway.app) pe jao
2. **"Start a New Project"** click karo
3. **GitHub account se login karo**

---

### Step 2 — GitHub Repo Connect Karo

1. **"Deploy from GitHub repo"** click karo
2. Railway GitHub access maangega — allow karo
3. **`SIH-2k26`** repo select karo
4. Railway automatically detect karega ki ye Django project hai ✅

---

### Step 3 — PostgreSQL Database Add Karo

1. Railway dashboard mein apna project open karo
2. **"+ New"** button click karo
3. **"Database"** → **"Add PostgreSQL"** select karo
4. Railway automatically `DATABASE_URL` environment variable set kar dega ✅

---

### Step 4 — Environment Variables Set Karo

Railway dashboard mein apni service ke **"Variables"** tab mein jao aur ye variables add karo:

| Variable | Value |
|----------|-------|
| `DJANGO_SECRET_KEY` | (neeche generator se generate karo) |
| `DJANGO_DEBUG` | `0` |
| `ALLOWED_HOSTS` | `yourapp.railway.app` (Railway deploy hone ke baad URL milega) |

**Secret Key generate karne ke liye** — apne PC mein run karo:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
Jo output aaye use `DJANGO_SECRET_KEY` ki value mein paste karo.

---

### Step 5 — Deploy Karo

- Variables save karne ke baad Railway **automatically redeploy** karega
- **"Deployments"** tab mein build logs dekho
- Green checkmark aane ka wait karo ✅
- Railway ek URL dega jaise: `https://yourapp.railway.app`

---

### Step 6 — Admin User Banao (Pehli Baar)

Railway dashboard mein apni service pe click karo → **"Shell"** tab:

```bash
cd backend
python manage.py createsuperuser
```

---

### Step 7 — ALLOWED_HOSTS Update Karo

Railway se jo URL mila (e.g. `sih-2k26-production.up.railway.app`), use:

1. Railway dashboard → **Variables** tab
2. `ALLOWED_HOSTS` ki value update karo apne actual domain se
3. Railway phir se redeploy karega

---

### ✅ Deployment Complete!

| Page | URL |
|------|-----|
| Homepage | `https://yourapp.railway.app/` |
| Login | `https://yourapp.railway.app/role-login.html` |
| Signup | `https://yourapp.railway.app/signup.html` |
| Admin Panel | `https://yourapp.railway.app/admin/` |

---

## 🌐 Free Deployment — Render.com (Alternative)

### Step 1 — Account Banao
[https://render.com](https://render.com) pe jao aur GitHub se login karo.

### Step 2 — Web Service Create Karo
1. **"New +"** → **"Web Service"** click karo
2. GitHub repo connect karo → `SIH-2k26` select karo
3. Ye settings fill karo:

| Setting | Value |
|---------|-------|
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && python manage.py migrate --noinput && gunicorn config.wsgi:application` |
| **Python Version** | `3.11.9` |

### Step 3 — Free PostgreSQL Add Karo
1. **"New +"** → **"PostgreSQL"** click karo
2. Free tier select karo
3. Database create hone ke baad `Internal Database URL` copy karo
4. Web Service ki **Environment** settings mein `DATABASE_URL` paste karo

### Step 4 — Environment Variables Add Karo
Render Web Service → **"Environment"** tab:

```
DJANGO_SECRET_KEY = (generated key)
DJANGO_DEBUG = 0
ALLOWED_HOSTS = yourapp.onrender.com
DATABASE_URL = (Render PostgreSQL ka URL)
```

> ⚠️ **Note:** Render free tier mein app 15 minute inactivity ke baad sleep ho jaata hai. Pehli request slow hogi. Railway mein ye problem nahi hoti.

---

## 📁 Project Structure

```
SIH-2k26/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── settings.py      — Django settings (production-ready)
│   │   ├── urls.py          — URL routing
│   │   └── wsgi.py
│   ├── accounts/            — User auth (login/signup/logout/roles)
│   └── prediction/          — ML flood risk prediction engine
│       ├── rainfall_model.pkl
│       └── risk_encoder.pkl
├── frontend/                — 21 HTML/CSS/JS pages
├── Procfile                 — Railway/Render start command
├── railway.json             — Railway config
├── runtime.txt              — Python 3.11.9
└── nixpacks.toml            — Build config
```

---

## ⚙️ What This System Does

- **AI/ML Flood Risk Prediction** — scikit-learn model predicts LOW/MODERATE/HIGH/EXTREME risk
- **Live Weather Data** — Open-Meteo API se real-time weather fetch karta hai
- **Role-based Auth** — Citizen aur Admin roles, Django session-based
- **Alert Management** — Flood alerts create aur manage karo
- **Risk Map** — Interactive map with risk visualization
- **Monitoring Stations** — Multiple location tracking

---

## 🔧 What Changed (from original)

- Django custom User model with Citizen/Admin roles
- Passwords stored using Django password hashing
- Session-based login/logout
- ML prediction endpoints (`/api/predict/`, `/api/auto-predict/`)
- Weather data from Open-Meteo API (free, no API key needed)
- Production-ready settings (WhiteNoise, PostgreSQL, env vars)
- Deployment files for Railway/Render