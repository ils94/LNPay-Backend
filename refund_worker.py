import asyncio
import db
import refund


# Same idea as the worker, but now with async
async def process_invoice(invoice):
    """Processes a single invoice."""
    # Wrap synchronous calls in asyncio.to_thread
    refund_address, amount = await asyncio.to_thread(db.get_refund_failure_details, invoice)

    if refund_address and amount:
        is_success = await asyncio.to_thread(refund.is_success, refund_address, amount)

        if is_success:
            print(f"Invoice {invoice} was successfully refunded!")
            await asyncio.to_thread(db.delete_refund_failure_invoice, invoice)
        else:
            print(f"Failed to refund invoice {invoice}, trying again in the next cycle...")


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
        invoices = await asyncio.to_thread(db.get_all_refund_failures)

        if invoices:
            total_invoices = len(invoices)
            print(f"Total invoices to refund: {total_invoices}")
            print(f"Invoices: {invoices}")

            if total_invoices > max_batch_size:
                num_batches = (total_invoices + max_batch_size - 1) // max_batch_size
                print(f"Splitting into {num_batches} batches.")

                for batch_index in range(0, total_invoices, max_batch_size):
                    batch = invoices[batch_index:batch_index + max_batch_size]
                    wait_time = len(batch) * 0.40
                    print(f"Processing batch {batch_index // max_batch_size + 1}/{num_batches}: {batch}")

                    await process_batch(batch, wait_time)
            else:
                wait_time = total_invoices * 0.40
                print(f"Processing all invoices in a single batch: {invoices}")

                await process_batch(invoices, wait_time)
        else:
            print("No invoices to refund. Waiting...")
            await asyncio.sleep(1)  # Default wait time if no invoices are found


# Run the asyncio event loop
asyncio.run(rerun_refund())
