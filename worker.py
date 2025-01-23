import db
import checkstatus
import time


def check_invoice_status():
    # Dynamically increases the wait time for using the Strike API based on the number of UNPAID invoices
    # in the database. To prevent abuse by users generating a large number of invoices, you should check if
    # the user already has a valid unpaid invoice. If so, replace the existing unpaid invoice with the newly
    # generated one, or simply display the old unpaid invoice to the user.

    # Allow the user to decide whether to delete the old invoice and generate a new one, or pay the existing one.

    # Additionally, show the user how much time is left to pay the current invoice.

    # This worker will create batches up to 600 invoices and run each batch in cycles,
    # expired invoices will be deleted (invoices has a lifetime of 1 hour).

    # This project aims to create a generic backend so anyone can implement it in their projects.
    # You should change the code based on your project needs.

    # Define the maximum batch size for API limits
    max_batch_size = 600

    while True:
        invoices = db.get_unpaid_invoices()

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
                    wait_time = len(batch) * 0.65  # Dynamic wait time based on batch size
                    print(f"Processing batch {batch_index // max_batch_size + 1}/{num_batches}: {batch}")

                    process_batch(batch)
                    print(f"Waiting {wait_time:.2f} seconds before the next batch...")
                    time.sleep(wait_time)
            else:
                # If total invoices <= max_batch_size, process them all at once
                wait_time = total_invoices * 0.65  # Dynamic wait time
                print(f"Processing all invoices in a single batch: {invoices}")

                process_batch(invoices)
                print(f"Waiting {wait_time:.2f} seconds before the next cycle...")
                time.sleep(wait_time)
        else:
            # If no unpaid invoices are found, wait before checking again
            print("No unpaid invoices found. Waiting...")
            time.sleep(30)  # Default wait time if no invoices are found


def process_batch(batch):
    """Processes a batch of invoices."""
    for invoice in batch:
        status = checkstatus.paid_invoice(invoice)
        print(f"{invoice} status: {status}")

        if status.upper() == 'PAID':
            db.set_invoice_paid(invoice)
            delivered = db.get_delivered_status(invoice)

            if delivered == 'NO':
                print(f"Setting {invoice} as delivered.")

                # Add here your logic to delivery your product and change the delivery status on
                # your local database after

                db.set_invoice_delivered(invoice)
        else:
            is_valid = db.is_invoice_valid(invoice)
            print(f"Is invoice still valid: {is_valid}")

            if not is_valid:
                print(f"Invoice {invoice} is UNPAID but expired. Deleting from the local database...")
                db.delete_invoice_by_id(invoice)


check_invoice_status()
