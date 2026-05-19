# 🏋️ Gym Management Dashboard

Beginner-friendly full-stack gym management dashboard built with:

- **FastAPI** (Python web framework)
- **SQLite** + **SQLAlchemy** (database)
- **Jinja2** templates
- **Tailwind CSS** (via CDN — no build step)
- **Vanilla JavaScript**
- **Chart.js** (revenue + analytics charts)

Runs from a single FastAPI server. Optimized for free deployment on Render or Railway.

---

## ✨ Features

- Admin login / logout (session-based)
- Dashboard with KPIs + revenue & member-growth charts
- Member CRUD with profile photo upload, search & pagination
- Trainer CRUD + assign to members
- Attendance: manual check-in/out + QR-style quick check-in
- Membership plans (Monthly / Quarterly / Yearly) + pending dues
- Analytics: revenue, active vs inactive, peak hours, top members
- Responsive sidebar layout + Dark/Light mode toggle
- Pre-seeded sample data

---

## 🚀 Quick Start (Local)

```bash
# 1. (Optional) create virtualenv
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install deps
pip install -r requirements.txt

# 3. Run the server
uvicorn main:app --reload
```

Open http://localhost:8000 and log in with:

```
Username: admin
Password: admin123
```

The SQLite DB (`gym.db`) and sample data are created automatically on first boot.

---

## 📁 Project Structure

```
gym/
├── main.py              # FastAPI entrypoint
├── database.py          # SQLAlchemy engine + session
├── models.py            # ORM models (Admin, Member, Trainer, ...)
├── auth.py              # Password hashing + login_required dep
├── seed.py              # Inserts dummy data
├── requirements.txt
├── Procfile             # For Render/Railway
├── routes/
│   ├── auth_routes.py
│   ├── dashboard.py
│   ├── members.py
│   ├── trainers.py
│   ├── attendance.py
│   ├── plans.py
│   └── analytics.py
├── templates/           # Jinja2 HTML (Tailwind + Chart.js inline)
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── members.html
│   ├── trainers.html
│   ├── attendance.html
│   ├── plans.html
│   ├── analytics.html
│   └── error.html
└── static/
    ├── css/
    ├── js/
    └── uploads/         # Member profile images
```

---

## ☁️ Deploy to Render (free)

1. Push this folder to a GitHub repo.
2. On https://render.com → **New → Web Service** → connect your repo.
3. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - (Or rely on the included `Procfile`.)
4. Add an environment variable (recommended):
   - `SESSION_SECRET` = any long random string

Done — Render serves your app at `https://your-app.onrender.com`.

> Note: Free Render disks are ephemeral. For persistent `gym.db` and uploads,
> attach a Render disk and mount it at the project root.

## ☁️ Deploy to Railway

1. Create new project → Deploy from GitHub repo.
2. Railway auto-detects Python and uses the `Procfile`.
3. Add `SESSION_SECRET` env var.

---

## 🔐 Change Admin Password

Run a Python shell:

```python
from database import SessionLocal
from models import Admin
from auth import hash_password

db = SessionLocal()
admin = db.query(Admin).filter(Admin.username=='admin').first()
admin.password_hash = hash_password('your-new-password')
db.commit()
```

---

## 🧠 Beginner Notes

- All Python files include comments explaining what each section does.
- Tailwind is loaded via CDN — no Node.js / build step required.
- Chart.js is loaded via CDN and used inline inside the templates.
- The `login_required` dependency protects every dashboard route.
- Want to reset the DB? Delete `gym.db` and restart the server.

Happy lifting! 💪
