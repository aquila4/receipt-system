from app.extensions import db
from flask_login import UserMixin



class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))

    role = db.Column(db.String(20), default="admin")

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))