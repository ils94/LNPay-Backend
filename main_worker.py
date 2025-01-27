import asyncio
import db
import checkstatus
import refund


# Main worker to check for unpaid invoices and expired invoices.
async def process_invoice(invoice):
    """Processes a single invoice."""
    # Wrap the synchronous call in asyncio.to_thread to make it non-blocking
    status = await asyncio.to_thread(checkstatus.paid_invoice, invoice)
    print(f"{invoice} status: {status}")

    if status.upper() == 'PAID':
        is_valid = await asyncio.to_thread(db.is_invoice_valid, invoice)

        if is_valid:
            await asyncio.to_thread(db.set_invoice_paid, invoice)
            delivered = await asyncio.to_thread(db.get_delivered_status, invoice)

            if delivered == 'NO':
                print(f"Setting {invoice} as delivered.")
                # Add your delivery logic here and update delivery status in the database
                await asyncio.to_thread(db.set_invoice_delivered, invoice)
        else:
            print(f"Refunding invoice because it was not paid in time: {invoice}")

            refund_address = await asyncio.to_thread(db.get_refund_address, invoice)
            amount = await asyncio.to_thread(db.get_amount_by_invoice_id, invoice)

            # Wrap synchronous refund.is_success in asyncio.to_thread
            is_success = await asyncio.to_thread(refund.is_success, refund_address, amount)

            if is_success:
                print(f"Deleting {invoice} from invoices database...")
                await asyncio.to_thread(db.delete_invoice_by_id, invoice)
            else:
                print("Refund API failed. Moving invoice to refund_failure table...")
                await asyncio.to_thread(db.copy_to_refund_failure, invoice)
                await asyncio.to_thread(db.delete_invoice_by_id, invoice)
    else:
        is_valid = await asyncio.to_thread(db.is_invoice_valid, invoice)
        print(f"Is invoice still valid: {is_valid}")

        if not is_valid:
            print(f"Invoice {invoice} is UNPAID and expired. Moving to expired table...")
            await asyncio.to_thread(db.copy_to_expired, invoice)
            await asyncio.to_thread(db.delete_invoice_by_id, invoice)


async def process_batch(batch, wait_time):
    """Processes a batch of invoices asynchronously."""
    tasks = [process_invoice(invoice) for invoice in batch]
    await asyncio.gather(*tasks)
    print(f"Batch processed. Waiting {wait_time:.2f} seconds before next batch...")
    await asyncio.sleep(wait_time)


async def check_invoice_status():
    """Main function to check and process unpaid invoices."""
    max_batch_size = 1000

    while True:
        # Wrap this in asyncio.to_thread since it's a blocking call
        invoices = await asyncio.to_thread(db.get_unpaid_invoices)

        if invoices:
            total_invoices = len(invoices)
            print(f"Total unpaid invoices: {total_invoices}")
            print(f"Invoices: {invoices}")

            if total_invoices > max_batch_size:
                num_batches = (total_invoices + max_batch_size - 1) // max_batch_size
                print(f"Splitting into {num_batches} batches.")

                for batch_index in range(0, total_invoices, max_batch_size):
                    batch = invoices[batch_index:batch_index + max_batch_size]
                    wait_time = len(batch) * 0.70
                    print(f"Processing batch {batch_index // max_batch_size + 1}/{num_batches}: {batch}")

                    await process_batch(batch, wait_time)
            else:
                wait_time = total_invoices * 0.70
                print(f"Processing all invoices in a single batch: {invoices}")

                await process_batch(invoices, wait_time)
        else:
            print("No unpaid invoices found. Waiting...")
            await asyncio.sleep(1)


# Run the asyncio event loop
asyncio.run(check_invoice_status())
