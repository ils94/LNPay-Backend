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
import db
import check_status
import refund_api
import delivery


# Use this to check the received invoice from the webhook
async def check_state(invoice):
    is_paid = await asyncio.to_thread(db.is_invoice_paid, invoice)

    if is_paid:
        print(f"{invoice} was already processed.")
        return

    status = await asyncio.to_thread(check_status.paid_invoice, invoice)
    print(f"{invoice} status: {status}")

    if status.upper() != 'PAID':
        return  # Skip further processing if not paid

    is_valid = await asyncio.to_thread(db.is_invoice_valid, invoice)

    if not is_valid:
        await handle_failed_invoice(invoice)
        return

    await process_paid_invoice(invoice)


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

        await delivery.logic()

        await asyncio.to_thread(db.set_invoice_delivered, invoice)
