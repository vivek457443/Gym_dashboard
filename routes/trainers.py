# routes/trainers.py - CRUD for trainers
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Trainer
from auth import login_required

router = APIRouter(prefix="/trainers")
templates = Jinja2Templates(directory="templates")


@router.get("")
def list_trainers(request: Request,
                  user: str = Depends(login_required),
                  db: Session = Depends(get_db)):
    trainers = db.query(Trainer).all()
    return templates.TemplateResponse("trainers.html", {
        "request": request, "user": user, "trainers": trainers,
        "active_page": "trainers",
    })


@router.post("/add")
def add_trainer(user: str = Depends(login_required),
                db: Session = Depends(get_db),
                name: str = Form(...),
                phone: str = Form(""), email: str = Form(""),
                specialization: str = Form(""),
                schedule: str = Form("")):
    t = Trainer(name=name, phone=phone, email=email,
                specialization=specialization, schedule=schedule)
    db.add(t); db.commit()
    return RedirectResponse("/trainers", status_code=303)


@router.post("/edit/{tid}")
def edit_trainer(tid: int,
                 user: str = Depends(login_required),
                 db: Session = Depends(get_db),
                 name: str = Form(...),
                 phone: str = Form(""), email: str = Form(""),
                 specialization: str = Form(""),
                 schedule: str = Form("")):
    t = db.query(Trainer).get(tid)
    if t:
        t.name = name; t.phone = phone; t.email = email
        t.specialization = specialization; t.schedule = schedule
        db.commit()
    return RedirectResponse("/trainers", status_code=303)


@router.get("/delete/{tid}")
def delete_trainer(tid: int,
                   user: str = Depends(login_required),
                   db: Session = Depends(get_db)):
    t = db.query(Trainer).get(tid)
    if t:
        db.delete(t); db.commit()
    return RedirectResponse("/trainers", status_code=303)
