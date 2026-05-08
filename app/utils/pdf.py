from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generate_receipt_pdf(receipt):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    # ======================
    # SAFE PATHS (IMPORTANT FIX)
    # ======================
    base_dir = os.path.dirname(os.path.abspath(__file__))

    signature_path = os.path.join(base_dir, "../static/signature.png")
    stamp_path = os.path.join(base_dir, "../static/stamp.png")

    # ======================
    # HEADER
    # ======================
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(300, 770, "GREAT MARCY SONS LIMITED")

    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawCentredString(300, 750, "GMC Realty (Property Division)")

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(300, 730, "OFFICIAL RECEIPT")

    pdf.line(50, 720, 550, 720)

    # ======================
    # DETAILS
    # ======================
    y = 680
    line_height = 24

    def row(label, value):
        nonlocal y
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(60, y, f"{label}:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(180, y, str(value))
        y -= line_height

    row("Receipt No", receipt.receipt_number)
    row("Customer", receipt.customer_name)
    row("Email", receipt.customer_email or "N/A")
    row("Description", receipt.description or "N/A")
    row("Date", receipt.created_at.strftime("%d %b %Y"))

    # ======================
    # AMOUNT BOX
    # ======================
    pdf.setLineWidth(2)
    pdf.rect(60, 420, 480, 60)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(80, 445, "TOTAL AMOUNT")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(300, 445, f"₦{receipt.amount:,.2f}")

    # ======================
    # STAMP (FIXED POSITION)
    # ======================
    try:
        pdf.drawImage(
            stamp_path,
            70,
            250,
            width=110,
            height=110,
            mask='auto'
        )
    except Exception as e:
        print("STAMP ERROR:", e)

    # ======================
    # SIGNATURE (FIXED POSITION)
    # ======================
    try:
        pdf.drawImage(
            signature_path,
            350,
            270,
            width=140,
            height=60,
            mask='auto'
        )
        pdf.setFont("Helvetica", 9)
        pdf.drawString(350, 260, "Authorized Signature")
    except Exception as e:
        print("SIGNATURE ERROR:", e)

    # ======================
    # CONTACT SECTION (FIXED SPACING)
    # ======================
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 140, "Contact Us")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, 125, "Email: info@greatmarcysonslimited.com")
    pdf.drawString(60, 110, "Phone: +234 913 907 0404")
    pdf.drawString(
        60,
        95,
        "Address: KULENDE AREA, KM5 OLD JEBBA ROAD, Sango Rd, Ilorin 240101, Kwara"
    )

    # ======================
    # FOOTER
    # ======================
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawCentredString(300, 50, "Thank you for your business")

    pdf.save()
    buffer.seek(0)

    return buffer