from flask import Blueprint, flash, request, render_template, redirect, url_for, make_response
from flask_login import login_required, current_user
from sqlalchemy import func
from io import BytesIO
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.utils.pdf import generate_receipt_pdf
from app.extensions import db
from app.models.receipt import Receipt
from app.utils.generator import generate_receipt_number
from app.utils.email import send_receipt_email

receipt_bp = Blueprint('receipt', __name__)

# ======================
# DASHBOARD
# ======================
@receipt_bp.route("/")
@login_required
def dashboard():

    search = request.args.get("q")

    query = Receipt.query.filter_by(company_id=current_user.company_id)

    if search:
        query = query.filter(Receipt.customer_name.ilike(f"%{search}%"))

    receipts = query.order_by(Receipt.id.desc()).all()

    total_receipts = query.count()

    total_amount = db.session.query(func.sum(Receipt.amount)).filter_by(
        company_id=current_user.company_id
    ).scalar() or 0

    today_total = db.session.query(func.sum(Receipt.amount)).filter(
        Receipt.company_id == current_user.company_id,
        func.date(Receipt.created_at) == func.date(func.now())
    ).scalar() or 0

    return render_template(
        "dashboard.html",
        receipts=receipts,
        total_receipts=total_receipts,
        total_amount=total_amount,
        today_total=today_total
    )

# ======================
# CREATE RECEIPT (EMAIL FIXED HERE)
# ======================
@receipt_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_receipt():

    if request.method == "GET":
        return render_template("create_receipt.html")

    data = request.form

    if not data.get("customer_name") or not data.get("amount"):
        flash("Missing fields", "danger")
        return redirect(url_for("receipt.create_receipt"))

    try:
        amount = float(data["amount"])
    except:
        flash("Invalid amount", "danger")
        return redirect(url_for("receipt.create_receipt"))

    receipt = Receipt(
        receipt_number=generate_receipt_number(),
        customer_name=data['customer_name'],
        customer_email=data.get("customer_email"),
        amount=amount,
        description=data.get('description', ''),
        user_id=current_user.id,
        company_id=current_user.company_id
    )

    db.session.add(receipt)
    db.session.commit()

    # ======================
    # SEND EMAIL (RESEND)
    # ======================
    try:
        send_receipt_email(receipt)
        print("Email sent successfully")
    except Exception as e:
        print("Email failed:", e)

    flash("Receipt created successfully!", "success")
    return redirect(url_for("receipt.dashboard"))

# ======================
# VERIFY RECEIPT
# ======================
@receipt_bp.route("/verify/<code>")
def verify_receipt(code):

    receipt = Receipt.query.filter_by(receipt_number=code).first()

    if not receipt:
        return "Receipt not found", 404

    return render_template("verify_receipt.html", receipt=receipt)

# ======================
# VIEW RECEIPT
# ======================
@receipt_bp.route("/<int:id>")
@login_required
def view_receipt(id):

    receipt = Receipt.query.get_or_404(id)
    return render_template("view_receipt.html", receipt=receipt)

# ======================
# PDF DOWNLOAD
# ======================


@receipt_bp.route("/<receipt_number>/pdf")
@login_required
def receipt_pdf(receipt_number):

    receipt = Receipt.query.filter_by(receipt_number=receipt_number).first_or_404()

    pdf_buffer = generate_receipt_pdf(receipt)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=f"{receipt_number}.pdf"
    )