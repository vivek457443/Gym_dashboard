# routes/dashboard.py - dashboard home with KPIs and charts
from datetime import date, timedelta
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Member, Payment, Attendance
from auth import login_required

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(request: Request,
              user: str = Depends(login_required),
              db: Session = Depends(get_db)):
    today = date.today()
    total_members = db.query(Member).count()
    active = db.query(Member).filter(Member.expiry_date >= today).count()
    expiring = db.query(Member).filter(
        Member.expiry_date >= today,
        Member.expiry_date <= today + timedelta(days=7)
    ).count()

    month_start = today.replace(day=1)
    monthly_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.paid_on >= month_start).scalar() or 0

    today_attendance = db.query(Attendance).filter(
        func.date(Attendance.check_in) == today).count()

    # Revenue last 6 months
    revenue_labels, revenue_data = [], []
    for i in range(5, -1, -1):
        m = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        nxt = (m + timedelta(days=32)).replace(day=1)
        amt = db.query(func.sum(Payment.amount)).filter(
            Payment.paid_on >= m, Payment.paid_on < nxt).scalar() or 0
        revenue_labels.append(m.strftime("%b %Y"))
        revenue_data.append(float(amt))

    # Member growth last 6 months (cumulative)
    growth_labels, growth_data = [], []
    for i in range(5, -1, -1):
        m = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        nxt = (m + timedelta(days=32)).replace(day=1)
        cnt = db.query(Member).filter(Member.joining_date < nxt).count()
        growth_labels.append(m.strftime("%b %Y"))
        growth_data.append(cnt)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "total_members": total_members,
        "active": active,
        "expiring": expiring,
        "monthly_revenue": monthly_revenue,
        "today_attendance": today_attendance,
        "revenue_labels": revenue_labels,
        "revenue_data": revenue_data,
        "growth_labels": growth_labels,
        "growth_data": growth_data,
        "active_page": "dashboard",
    })
