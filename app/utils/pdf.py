from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_receipt_pdf(receipt):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    # ======================
    # HEADER
    # ======================
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(300, 770, "GREAT MARCY SONS LIMITED")

    # SUB NAME (GMC Realty)
    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawCentredString(300, 750, "GMC Realty")

    # TITLE
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(300, 730, "OFFICIAL RECEIPT")

    pdf.line(50, 720, 550, 720)

    # ======================
    # DETAILS
    # ======================
    y = 680
    line_height = 25

    def row(label, value):
        nonlocal y
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(60, y, f"{label}:")
        pdf.setFont("Helvetica", 12)
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
    # SIGNATURE
    # ======================
    try:
        pdf.drawImage("app/static/signature.png", 350, 180, width=140, height=60, mask='auto')
        pdf.setFont("Helvetica", 9)
        pdf.drawString(350, 170, "Authorized Signature")
    except:
        pass  # prevents crash if image missing

    # ======================
    # STAMP
    # ======================
    try:
        pdf.drawImage("app/static/stamp.png", 80, 160, width=110, height=110, mask='auto')
    except:
        pass

    # ======================
    # CONTACT SECTION
    # ======================
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 120, "Contact Us")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, 105, "Email: info@greatmarcysonslimited.com")
    pdf.drawString(60, 90, "Phone: +234 913 907 0404")
    pdf.drawString(
        60,
        75,
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