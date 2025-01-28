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
import refund_api
import check_status


# Same idea as the main_worker, but now with async
async def process_invoice(invoice):
    """Processes a single invoice."""
    # Wrap synchronous calls in asyncio.to_thread
    status = await asyncio.to_thread(check_status.paid_invoice, invoice)
    print(f"{invoice} status: {status}")

    if status.upper() == 'PAID':

        refund_address, amount = await asyncio.to_thread(db.get_expired_details, invoice)

        if refund_address and amount:
            is_success = await asyncio.to_thread(refund_api.is_success, refund_address, amount)

            if is_success:
                print(f"Invoice {invoice} was successfully refunded!")
                await asyncio.to_thread(db.delete_expired_invoice, invoice)
            else:
                print(f"Failed to refund invoice {invoice}, trying again in the next cycle...")
    else:
        is_valid = await asyncio.to_thread(db.is_invoice_valid_one_hour, invoice)

        if not is_valid:
            print(f"Deleting {invoice}, as its expiration was due on the Strike API side...")
            await asyncio.to_thread(db.delete_expired_invoice, invoice)


async def process_batch(batch, wait_time):
    """Processes a batch of invoices asynchronously."""
    tasks = [process_invoice(invoice) for invoice in batch]
    await asyncio.gather(*tasks)
    print(f"Batch processed. Waiting {wait_time:.2f} seconds before next batch...")
    await asyncio.sleep(wait_time)


async def rerun_refund():
    """Main function to rerun refund processes."""
    max_batch_size = 250

    while True:
        invoices = await asyncio.to_thread(db.get_all_expired)

        if invoices:
            total_invoices = len(invoices)
            print(f"Total invoices to refund: {total_invoices}")
            print(f"Invoices: {invoices}")

            if total_invoices > max_batch_size:
                num_batches = (total_invoices + max_batch_size - 1) // max_batch_size
                print(f"Splitting into {num_batches} batches.")

                for batch_index in range(0, total_invoices, max_batch_size):
                    batch = invoices[batch_index:batch_index + max_batch_size]
                    wait_time = len(batch) * 1
                    print(f"Processing batch {batch_index // max_batch_size + 1}/{num_batches}: {batch}")

                    await process_batch(batch, wait_time)
            else:
                wait_time = total_invoices * 1
                print(f"Processing all invoices in a single batch: {invoices}")

                await process_batch(invoices, wait_time)
        else:
            print("No expired invoices. Waiting...")
            await asyncio.sleep(1)  # Default wait time if no invoices are found


# Run the asyncio event loop
asyncio.run(rerun_refund())
