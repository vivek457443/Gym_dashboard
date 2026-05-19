# auth.py - simple session-based auth helpers
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        return False


def login_required(request: Request):
    """Use as a FastAPI dependency. Redirects to /login if no session."""
    if not request.session.get("admin"):
        # Raise HTTPException with 302 redirect via a custom mechanism:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/login"},
        )
    return request.session["admin"]
