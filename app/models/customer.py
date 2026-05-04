from app.extensions import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)

    phone = db.Column(db.String(30), nullable=True)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    company = db.relationship("Company", backref="customers")