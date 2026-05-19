"""
main.py - FastAPI entrypoint for the Gym Management Dashboard.
Run:  uvicorn main:app --reload
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from starlette.middleware.sessions import SessionMiddleware

from database import engine, Base
from seed import seed
from routes import auth_routes, dashboard, members, trainers, attendance, plans, analytics

# Create DB tables + seed sample data on first boot
Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="Gym Management Dashboard")

# Session middleware (cookie based). Change secret in production via env var.
SECRET = os.getenv("SESSION_SECRET", "change-me-in-prod-please")
app.add_middleware(SessionMiddleware, secret_key=SECRET)

# Static files (CSS, JS, uploaded images)
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Register routers
app.include_router(auth_routes.router)
app.include_router(dashboard.router)
app.include_router(members.router)
app.include_router(trainers.router)
app.include_router(attendance.router)
app.include_router(plans.router)
app.include_router(analytics.router)


@app.get("/")
def root(request: Request):
    if request.session.get("admin"):
        return RedirectResponse("/dashboard")
    return RedirectResponse("/login")


# Convert 307 auth redirects into proper browser redirects
@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException):
    if exc.status_code == 307 and exc.headers and "Location" in exc.headers:
        return RedirectResponse(exc.headers["Location"])
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )
