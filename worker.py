import db
import checkstatus


def check_invoice_status():
    invoices = db.get_unpaid_invoices()

    for invoice in invoices:
        status = checkstatus.paid_invoice(invoice)

        if status.upper() == 'PAID':
            db.set_invoice_paid(invoice)

            delivered = db.get_delivered_status(invoice)

            if delivered == 'NO':
                db.set_invoice_delivered(invoice)

        else:
            if not db.is_invoice_valid(invoice):
                db.delete_invoice_by_id(invoice)
