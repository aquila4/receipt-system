from flask_mail import Message
from app.extensions import mail

def send_receipt_email(receipt):
    msg = Message(
        subject=f"Your Receipt #{receipt.receipt_number}",
        recipients=[receipt.customer_email]
    )

    msg.body = f"""
Hello {receipt.customer_name},

Your payment receipt has been generated.

Receipt No: {receipt.receipt_number}
Amount: ₦{receipt.amount}
Description: {receipt.description}

Thank you.
"""

    mail.send(msg)