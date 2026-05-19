# routes/attendance.py - check-in / check-out and history
from datetime import datetime, date
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import get_db
from models import Attendance, Member
from auth import login_required

router = APIRouter(prefix="/attendance")
templates = Jinja2Templates(directory="templates")


@router.get("")
def attendance_page(request: Request,
                    user: str = Depends(login_required),
                    db: Session = Depends(get_db)):
    today = date.today()
    today_records = db.query(Attendance).filter(
        func.date(Attendance.check_in) == today).order_by(
        desc(Attendance.check_in)).all()
    history = db.query(Attendance).order_by(
        desc(Attendance.check_in)).limit(50).all()
    members = db.query(Member).order_by(Member.name).all()
    return templates.TemplateResponse("attendance.html", {
        "request": request, "user": user,
        "today_records": today_records, "history": history,
        "members": members, "today": today,
        "active_page": "attendance",
    })


@router.post("/checkin")
def checkin(member_id: int = Form(...),
            user: str = Depends(login_required),
            db: Session = Depends(get_db)):
    db.add(Attendance(member_id=member_id, check_in=datetime.now()))
    db.commit()
    return RedirectResponse("/attendance", status_code=303)


@router.get("/checkout/{aid}")
def checkout(aid: int,
             user: str = Depends(login_required),
             db: Session = Depends(get_db)):
    a = db.query(Attendance).get(aid)
    if a and not a.check_out:
        a.check_out = datetime.now()
        db.commit()
    return RedirectResponse("/attendance", status_code=303)
