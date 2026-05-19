# models.py - SQLAlchemy ORM models
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from database import Base


class Admin(Base):
    """Admin user for login."""
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)


class Trainer(Base):
    __tablename__ = "trainers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(120))
    specialization = Column(String(100))
    schedule = Column(String(255))  # e.g. "Mon-Fri 6am-2pm"
    members = relationship("Member", back_populates="trainer")


class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(120))
    age = Column(Integer)
    gender = Column(String(10))
    joining_date = Column(Date, default=date.today)
    membership_type = Column(String(20))  # Monthly / Quarterly / Yearly
    expiry_date = Column(Date)
    fee = Column(Float, default=0.0)
    payment_status = Column(String(20), default="Paid")  # Paid / Pending
    image = Column(String(255))  # filename in /static/uploads
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=True)
    active = Column(Boolean, default=True)

    trainer = relationship("Trainer", back_populates="members")
    attendances = relationship("Attendance", back_populates="member",
                               cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="member",
                            cascade="all, delete-orphan")


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    check_in = Column(DateTime, default=datetime.utcnow)
    check_out = Column(DateTime, nullable=True)
    member = relationship("Member", back_populates="attendances")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount = Column(Float, nullable=False)
    paid_on = Column(Date, default=date.today)
    plan = Column(String(20))  # Monthly / Quarterly / Yearly
    member = relationship("Member", back_populates="payments")
