from flask_mail import Message
from flask import current_app, render_template_string
from app.extensions import mail
from app.utils.pdf import generate_receipt_pdf


def send_receipt_email(receipt):

    if not receipt.customer_email:
        return

    html = render_template_string("""
    <div style="font-family: Arial, sans-serif; background:#f5f7fb; padding:40px 20px;">

        <div style="max-width:600px; margin:auto; background:white; border-radius:12px;
                    overflow:hidden; box-shadow:0 10px 25px rgba(0,0,0,0.06);">

            <!-- HEADER -->
            <div style="background:#0f172a; color:white; padding:30px; text-align:center;">
                <h2 style="margin:0; font-size:20px; letter-spacing:0.5px;">
                    GREAT MARCY SONS LIMITED
                </h2>

                <p style="margin:6px 0 0; font-size:13px; opacity:0.85;">
                    GMC Realty (Property Division)
                </p>

                <p style="margin:4px 0 0; font-size:12px; opacity:0.6;">
                    Official Receipt Notification
                </p>
            </div>

            <!-- BODY -->
            <div style="padding:30px; color:#111827;">

                <h3 style="margin-top:0; font-size:18px;">
                    Hello {{ receipt.customer_name }},
                </h3>

                <p style="font-size:14px; color:#374151; line-height:1.6;">
                    Your payment has been successfully processed. Below are your receipt details.
                </p>

                <!-- DETAILS BOX -->
                <div style="background:#f9fafb; padding:18px; border-radius:10px; margin-top:20px;">

                    <p style="margin:6px 0;">
                        <strong>Receipt No:</strong> {{ receipt.receipt_number }}
                    </p>

                    <p style="margin:6px 0;">
                        <strong>Amount:</strong> ₦{{ "{:,.2f}".format(receipt.amount) }}
                    </p>

                    <p style="margin:6px 0;">
                        <strong>Date:</strong> {{ receipt.created_at.strftime("%d %b %Y") }}
                    </p>

                </div>

                <p style="margin-top:18px; font-size:14px; color:#374151;">
                    Your official receipt is attached as a downloadable PDF.
                </p>

                <!-- BUTTON -->
                <div style="text-align:center; margin-top:25px;">
                    <a href="{{ verify_url }}"
                       style="background:#2563eb; color:white; padding:12px 22px;
                       text-decoration:none; border-radius:8px; display:inline-block;
                       font-weight:bold; font-size:14px;">
                        Verify Receipt
                    </a>
                </div>

                <p style="margin-top:25px; font-size:12px; color:#6b7280; text-align:center;">
                    If you did not expect this email, please ignore it.
                </p>

            </div>

            <!-- FOOTER -->
            <div style="background:#f1f5f9; padding:18px; text-align:center; font-size:12px; color:#374151;">
                <p style="margin:4px 0;">info@greatmarcysonslimited.com</p>
                <p style="margin:4px 0;">+234 913 907 0404</p>
            </div>

        </div>
    </div>
    """,
    receipt=receipt,
    verify_url=f"{current_app.config.get('BASE_URL','')}/receipt/verify/{receipt.receipt_number}"
    )

    # ======================
    # EMAIL MESSAGE
    # ======================
    msg = Message(
        subject=f"Receipt Confirmation - {receipt.receipt_number}",
        recipients=[receipt.customer_email]
    )

    msg.html = html
    msg.body = f"Your receipt {receipt.receipt_number} has been generated and attached."

    # ======================
    # PDF ATTACHMENT
    # ======================
    pdf_buffer = generate_receipt_pdf(receipt)

    msg.attach(
        filename=f"{receipt.receipt_number}.pdf",
        content_type="application/pdf",
        data=pdf_buffer.read()
    )

    # ======================
    # SEND EMAIL
    # ======================
    mail.send(msg)