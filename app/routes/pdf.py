from flask import make_response, render_template
from weasyprint import HTML
from app.models.receipt import Receipt
from app.routes.receipt_routes import receipt_bp


@receipt_bp.route("/<receipt_number>/pdf")
def download_pdf(receipt_number):

    receipt = Receipt.query.filter_by(receipt_number=receipt_number).first()

    # 🚨 SAFE CHECK
    if not receipt:
        return {"error": "Receipt not found"}, 404

    html = render_template("receipt.html", receipt=receipt)

    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f"inline; filename={receipt_number}.pdf"
    )

    return response