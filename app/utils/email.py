from flask_mail import Message
from flask import current_app, render_template_string
from app.extensions import mail
from app.utils.pdf import generate_receipt_pdf


def send_receipt_email(receipt):

    if not receipt.customer_email:
        return

    # ======================
    # HTML EMAIL TEMPLATE
    # ======================
    html = render_template_string("""
    <div style="font-family: Arial, sans-serif; background:#f5f7fb; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; border-radius:10px; overflow:hidden; box-shadow:0 5px 15px rgba(0,0,0,0.05);">

            <!-- HEADER -->
            <div style="background:#0f172a; color:white; padding:20px; text-align:center;">
                <h2 style="margin:0;">GREAT MARCY SONS LIMITED</h2>
                <p style="margin:5px 0 0; font-size:14px; opacity:0.8;">GMC Realty</p>
            </div>

            <!-- BODY -->
            <div style="padding:25px;">
                <h3 style="margin-top:0;">Hello {{ receipt.customer_name }},</h3>

                <p>Thank you for your payment. Your receipt details are below:</p>

                <div style="background:#f9fafb; padding:15px; border-radius:8px;">
                    <p><strong>Receipt No:</strong> {{ receipt.receipt_number }}</p>
                    <p><strong>Amount:</strong> ₦{{ "{:,.2f}".format(receipt.amount) }}</p>
                    <p><strong>Date:</strong> {{ receipt.created_at.strftime("%d %b %Y") }}</p>
                </div>

                <p style="margin-top:20px;">
                    Your official receipt is attached as a PDF.
                </p>

                <!-- VERIFY BUTTON -->
                <div style="text-align:center; margin:25px 0;">
                    <a href="{{ verify_url }}"
                       style="background:#2563eb; color:white; padding:12px 20px; text-decoration:none; border-radius:6px; font-weight:bold;">
                       Verify Receipt
                    </a>
                </div>

                <p>If you have any questions, feel free to contact us.</p>
            </div>

            <!-- FOOTER -->
            <div style="background:#f1f5f9; padding:15px; font-size:12px; text-align:center;">
                <p>Email: info@greatmarcysonslimited.com</p>
                <p>Phone: +234 913 907 0404</p>
                <p>KULENDE AREA, KM5 OLD JEBBA ROAD, Ilorin, Kwara</p>
            </div>

        </div>
    </div>
    """, receipt=receipt,
       verify_url=f"{current_app.config.get('BASE_URL', '')}/receipt/verify/{receipt.receipt_number}"
    )

    # ======================
    # EMAIL OBJECT
    # ======================
    msg = Message(
        subject=f"Your Receipt {receipt.receipt_number}",
        recipients=[receipt.customer_email]
    )

    msg.html = html

    # ======================
    # ATTACH PDF
    # ======================
    pdf_buffer = generate_receipt_pdf(receipt)

    msg.attach(
        filename=f"{receipt.receipt_number}.pdf",
        content_type="application/pdf",
        data=pdf_buffer.read()
    )

    # ======================
    # SEND
    # ======================
    mail.send(msg)