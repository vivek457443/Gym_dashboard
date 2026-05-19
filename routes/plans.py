# routes/plans.py - membership plans + dues
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Member, Payment
from auth import login_required

router = APIRouter(prefix="/plans")
templates = Jinja2Templates(directory="templates")

PLANS = [
    {"name": "Monthly",   "days": 30,  "price": 1500},
    {"name": "Quarterly", "days": 90,  "price": 4000},
    {"name": "Yearly",    "days": 365, "price": 12000},
]


@router.get("")
def plans_page(request: Request,
               user: str = Depends(login_required),
               db: Session = Depends(get_db)):
    pending = db.query(Member).filter(
        Member.payment_status == "Pending").all()
    return templates.TemplateResponse("plans.html", {
        "request": request, "user": user, "plans": PLANS,
        "pending": pending, "active_page": "plans",
    })


@router.post("/pay/{mid}")
def mark_paid(mid: int,
              user: str = Depends(login_required),
              db: Session = Depends(get_db)):
    m = db.query(Member).get(mid)
    if m:
        m.payment_status = "Paid"
        db.add(Payment(member_id=m.id, amount=m.fee, plan=m.membership_type))
        db.commit()
    return RedirectResponse("/plans", status_code=303)
