# routes/analytics.py - monthly revenue, active vs inactive, peak hours, top members
from datetime import date, timedelta
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import get_db
from models import Member, Payment, Attendance
from auth import login_required

router = APIRouter(prefix="/analytics")
templates = Jinja2Templates(directory="templates")


@router.get("")
def analytics_page(request: Request,
                   user: str = Depends(login_required),
                   db: Session = Depends(get_db)):
    today = date.today()

    # Monthly revenue (last 12 months)
    rev_labels, rev_data = [], []
    for i in range(11, -1, -1):
        m = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        nxt = (m + timedelta(days=32)).replace(day=1)
        amt = db.query(func.sum(Payment.amount)).filter(
            Payment.paid_on >= m, Payment.paid_on < nxt).scalar() or 0
        rev_labels.append(m.strftime("%b %y"))
        rev_data.append(float(amt))

    active = db.query(Member).filter(Member.expiry_date >= today).count()
    inactive = db.query(Member).filter(Member.expiry_date < today).count()

    # Peak hours (group by hour of check_in)
    hour_counts = dict.fromkeys(range(24), 0)
    rows = db.query(
        func.strftime("%H", Attendance.check_in).label("h"),
        func.count(Attendance.id)).group_by("h").all()
    for h, c in rows:
        try:
            hour_counts[int(h)] = c
        except Exception:
            pass
    peak_labels = [f"{h:02d}:00" for h in range(24)]
    peak_data = [hour_counts[h] for h in range(24)]

    # Top 5 most regular members (by attendance count)
    top_rows = db.query(
        Member, func.count(Attendance.id).label("c")
    ).join(Attendance, Attendance.member_id == Member.id) \
     .group_by(Member.id).order_by(desc("c")).limit(5).all()
    top_members = [{"name": m.name, "count": c} for m, c in top_rows]

    return templates.TemplateResponse("analytics.html", {
        "request": request, "user": user,
        "rev_labels": rev_labels, "rev_data": rev_data,
        "active": active, "inactive": inactive,
        "peak_labels": peak_labels, "peak_data": peak_data,
        "top_members": top_members,
        "active_page": "analytics",
    })
