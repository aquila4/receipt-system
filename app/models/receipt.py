from app.extensions import db
from datetime import datetime

class Receipt(db.Model):
    __tablename__ = "receipt"

    id = db.Column(db.Integer, primary_key=True)

    receipt_number = db.Column(db.String(50), unique=True)

    customer_name = db.Column(db.String(120))
    customer_email = db.Column(db.String(120))

    amount = db.Column(db.Float)
    description = db.Column(db.String(255))

    status = db.Column(db.String(20), default="PAID")

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    created_at = db.Column(db.DateTime, default=db.func.now())

    # ✅ ADD THIS (IMPORTANT)
    company = db.relationship("Company", backref="receipts")

    # (optional but recommended)
    user = db.relationship("User", backref="receipts")