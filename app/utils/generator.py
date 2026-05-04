def generate_receipt_number():
    from app.models.receipt import Receipt

    count = Receipt.query.count() + 1
    return f"REC-2026-{str(count).zfill(4)}"