from app.extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120))
    logo = db.Column(db.String(255))   # /static/logo.png
    stamp = db.Column(db.String(255))  # /static/stamp.png

    created_at = db.Column(db.DateTime, default=db.func.now())

