import db
import time
import refund


def rerun_refund():

    # The same idea as the worker, but with a different batch size and wait time, also the process batch is
    # much simpler

    max_batch_size = 250

    while True:
        invoices = db.get_all_refund_failures()

        if invoices:
            total_invoices = len(invoices)

            print(f"Total unpaid invoices: {total_invoices}")
            print(f"Invoices: {invoices}")

            # If there are more invoices than the max batch size, split into batches
            if total_invoices > max_batch_size:
                num_batches = (total_invoices + max_batch_size - 1) // max_batch_size  # Round up to cover all invoices
                print(f"Splitting into {num_batches} batches.")

                for batch_index in range(0, total_invoices, max_batch_size):
                    batch = invoices[batch_index:batch_index + max_batch_size]
                    wait_time = len(batch) * 0.30  # Dynamic wait time based on batch size
                    print(f"Processing batch {batch_index // max_batch_size + 1}/{num_batches}: {batch}")

                    process_batch(batch)
                    print(f"Waiting {wait_time:.2f} seconds before the next batch...")
                    time.sleep(wait_time)
            else:
                # If total invoices <= max_batch_size, process them all at once
                wait_time = total_invoices * 0.30  # Dynamic wait time
                print(f"Processing all invoices in a single batch: {invoices}")

                process_batch(invoices)
                print(f"Waiting {wait_time:.2f} seconds before the next cycle...")
                time.sleep(wait_time)
        else:
            # If no unpaid invoices are found, wait before checking again
            print("No invoices to refund. Waiting...")
            time.sleep(1)  # Default wait time if no invoices are found


def process_batch(batch):
    """Processes a batch of invoices."""
    for invoice in batch:

        refund_address, amount = db.get_refund_failure_details(invoice)

        if refund_address and amount:
            is_success = refund.is_success(refund_address, amount)

            if is_success:
                print(f"Invoice {invoice} was successfully refunded!")
                db.delete_refund_failure_invoice(invoice)
            else:
                print(f"Failed to refund invoice {invoice}, trying again in the next cycle...")


rerun_refund()
