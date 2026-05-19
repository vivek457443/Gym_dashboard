# seed.py - insert sample dummy data for first-time setup
from datetime import date, datetime, timedelta
import random
from database import SessionLocal, engine, Base
from models import Admin, Trainer, Member, Attendance, Payment
from auth import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Admin
        if not db.query(Admin).first():
            db.add(Admin(username="admin",
                         password_hash=hash_password("admin123")))

        # Trainers
        if not db.query(Trainer).first():
            trainers = [
                Trainer(name="Rahul Singh", phone="9000000001",
                        email="rahul@gym.com", specialization="Strength",
                        schedule="Mon-Fri 6am-2pm"),
                Trainer(name="Anita Sharma", phone="9000000002",
                        email="anita@gym.com", specialization="Yoga",
                        schedule="Mon-Sat 7am-11am"),
                Trainer(name="John Doe", phone="9000000003",
                        email="john@gym.com", specialization="Cardio",
                        schedule="Tue-Sun 4pm-9pm"),
            ]
            db.add_all(trainers)
            db.commit()

        # Members
        if not db.query(Member).first():
            plans = {"Monthly": (30, 1500),
                     "Quarterly": (90, 4000),
                     "Yearly": (365, 12000)}
            genders = ["Male", "Female"]
            names = ["Amit", "Priya", "Karan", "Neha", "Vikram", "Sara",
                     "Rohit", "Pooja", "Manish", "Divya", "Arjun", "Kavya"]
            trainers = db.query(Trainer).all()
            for i, n in enumerate(names):
                plan = random.choice(list(plans.keys()))
                days, fee = plans[plan]
                join = date.today() - timedelta(days=random.randint(1, 200))
                m = Member(
                    name=f"{n} Kumar",
                    phone=f"98{random.randint(10000000,99999999)}",
                    email=f"{n.lower()}@mail.com",
                    age=random.randint(18, 45),
                    gender=random.choice(genders),
                    joining_date=join,
                    membership_type=plan,
                    expiry_date=join + timedelta(days=days),
                    fee=fee,
                    payment_status=random.choice(["Paid", "Paid", "Pending"]),
                    trainer_id=random.choice(trainers).id,
                    active=True,
                )
                db.add(m)
            db.commit()

            # Attendance + payments
            members = db.query(Member).all()
            for m in members:
                for d in range(random.randint(3, 15)):
                    ci = datetime.now() - timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(6, 21))
                    db.add(Attendance(member_id=m.id,
                                      check_in=ci,
                                      check_out=ci + timedelta(hours=1)))
                db.add(Payment(member_id=m.id, amount=m.fee,
                               paid_on=m.joining_date,
                               plan=m.membership_type))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed complete. Login: admin / admin123")
