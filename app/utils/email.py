from flask import current_app, render_template_string
import requests
import base64
from app.utils.pdf import generate_receipt_pdf


def send_receipt_email(receipt):

    if not receipt.customer_email:
        return

    api_key = current_app.config.get("RESEND_API_KEY")
    if not api_key:
        print("Missing RESEND_API_KEY")
        return

    verify_url = f"{current_app.config.get('BASE_URL','')}/receipt/verify/{receipt.receipt_number}"

    html = render_template_string("""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial;
                background:#f5f7fb; padding:40px 15px;">

        <div style="max-width:620px; margin:auto; background:#ffffff;
                    border-radius:14px; overflow:hidden;
                    box-shadow:0 10px 30px rgba(0,0,0,0.08);">

            <!-- HEADER -->
            <div style="background:#0f172a; color:white; padding:28px; text-align:center;">
                <h2 style="margin:0; font-size:20px;">
                    GREAT MARCY SONS LIMITED
                </h2>
                <p style="margin:6px 0 0; font-size:13px; opacity:0.85;">
                    GMC Realty (Property Division)
                </p>
                <p style="margin:4px 0 0; font-size:11px; opacity:0.6;">
                    Official Receipt Notification
                </p>
            </div>

            <!-- BODY -->
            <div style="padding:28px; color:#111827;">

                <h3 style="margin:0 0 10px;">
                    Hello {{ receipt.customer_name }},
                </h3>

                <p style="font-size:14px; color:#374151;">
                    Your payment has been successfully processed.
                </p>

                <div style="margin-top:18px; background:#f9fafb;
                            padding:16px; border-radius:10px;
                            border:1px solid #e5e7eb;">

                    <p><strong>Receipt No:</strong> {{ receipt.receipt_number }}</p>
                    <p><strong>Amount:</strong> ₦{{ "{:,.2f}".format(receipt.amount) }}</p>
                    <p><strong>Date:</strong> {{ receipt.created_at.strftime("%d %b %Y") }}</p>

                </div>

                <p style="margin-top:18px; font-size:14px;">
                    Your official receipt is attached as a PDF.
                </p>

                <!-- BUTTON -->
                <div style="text-align:center; margin-top:24px;">
                    <a href="{{ verify_url }}"
                       target="_blank"
                       rel="noopener noreferrer"
                       style="background:#2563eb; color:white;
                       padding:12px 22px; border-radius:8px;
                       text-decoration:none; font-weight:600;
                       display:inline-block;">
                        View Receipt
                    </a>
                </div>

                <!-- MOBILE SAFE FALLBACK -->
                <div style="margin-top:18px; text-align:center; font-size:12px; color:#6b7280;">

                    <p style="margin-bottom:8px;">
                        If the button doesn’t work, tap and hold the link below:
                    </p>

                    <p style="word-break:break-all; padding:10px;
                              background:#f9fafb; border:1px solid #e5e7eb;
                              border-radius:8px;">
                        <a href="{{ verify_url }}"
                           target="_blank"
                           style="color:#2563eb; text-decoration:none; font-weight:600;">
                            {{ verify_url }}
                        </a>
                    </p>

                </div>

                <p style="margin-top:20px; font-size:12px; color:#9ca3af; text-align:center;">
                    If you received this by mistake, you can safely ignore this email.
                </p>

            </div>

            <!-- FOOTER -->
            <div style="background:#f1f5f9; padding:18px; text-align:center; font-size:12px;">
                <p>info@greatmarcysonslimited.com</p>
                <p>+234 913 907 0404</p>
            </div>

        </div>
    </div>
    """,
    receipt=receipt,
    verify_url=verify_url
    )

    # PDF
    pdf_buffer = generate_receipt_pdf(receipt)
    pdf_base64 = base64.b64encode(pdf_buffer.read()).decode()

    # RESEND PAYLOAD
    payload = {
        "from": "GMC Realty Support <info@contact.greatmarcysonslimited.com>",
        "to": receipt.customer_email,
        "subject": f"Receipt Confirmation - {receipt.receipt_number}",
        "html": html,
        "attachments": [
            {
                "filename": f"{receipt.receipt_number}.pdf",
                "content": pdf_base64
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.resend.com/emails",
        json=payload,
        headers=headers
    )

    print("EMAIL RESPONSE:", response.status_code, response.text)