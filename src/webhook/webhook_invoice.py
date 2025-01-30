# MIT License
#
# Copyright (c) 2025 ILS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
from src.database import db
from src.services import check_status, refund_api
from src.config import delivery


# Use this to check the received invoice from the webhook
async def check_state(invoice_id):
    is_paid = await asyncio.to_thread(db.is_invoice_paid, invoice_id)

    if is_paid:
        print(f"{invoice_id} was already processed.")
        return

    status = await asyncio.to_thread(check_status.paid_invoice, invoice_id)
    print(f"{invoice_id} status: {status}")

    if status.upper() != 'PAID':
        return  # Skip further processing if not paid

    is_valid = await asyncio.to_thread(db.is_invoice_valid, invoice_id)

    if not is_valid:
        await handle_failed_invoice(invoice_id)
        return

    await process_paid_invoice(invoice_id)


async def handle_failed_invoice(invoice):
    print(f"Refunding invoice because it was not paid in time: {invoice}")

    refund_address, amount = await asyncio.to_thread(db.get_refund_details, invoice)

    is_success = await asyncio.to_thread(refund_api.is_success, refund_address, amount)

    if is_success:
        print(f"Deleting {invoice} from invoices database...")

        await asyncio.to_thread(db.delete_invoice_by_id, invoice)

    else:
        print("Refund API failed. Moving invoice to refund_failure table...")

        await asyncio.to_thread(db.copy_to_refund_failure, invoice)
        await asyncio.to_thread(db.delete_invoice_by_id, invoice)


async def process_paid_invoice(invoice):
    await asyncio.to_thread(db.set_invoice_paid, invoice)

    delivered = await asyncio.to_thread(db.get_delivered_status, invoice)

    if delivered == 'NO':
        print(f"Setting {invoice} as delivered.")

        invoice = await asyncio.to_thread(db.get_invoice_lnurl, invoice)

        await delivery.logic(invoice)

        await asyncio.to_thread(db.set_invoice_delivered, invoice)
