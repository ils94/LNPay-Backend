import sqlite3
from datetime import datetime


# Function to create the SQLite database and table
def create_database():
    connection = sqlite3.connect("invoices.sqlite")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        currency TEXT,
        correlation TEXT,
        created TEXT,
        description TEXT,
        invoiceId TEXT,
        state TEXT,
        delivered TEXT,
        expiration TEXT,
        lnInvoice TEXT
    )
    ''')
    connection.commit()
    connection.close()


# Function to insert data into the SQLite database
def insert_invoice(json_data):
    # Extract relevant information from the JSON
    try:
        create_database()

        invoice = json_data['data']['invoice']
        quote = json_data['data']['quote']

        amount = float(invoice['amount']['amount'])
        currency = invoice['amount']['currency']
        correlation = invoice['correlationId']
        created = invoice['created']
        description = invoice['description']
        invoiceid = invoice['invoiceId']
        state = invoice['state']
        delivered = "NO"
        expiration = quote['expiration']
        lninvoice = quote['lnInvoice']

        # Insert into the database
        connection = sqlite3.connect("invoices.sqlite")
        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO invoices (
            amount, currency, correlation, created, description, 
            invoiceId, state, delivered, expiration, lnInvoice
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (amount, currency, correlation, created, description,
              invoiceid, state, delivered, expiration, lninvoice))

        connection.commit()
        connection.close()
        print("Invoice data inserted successfully.")
    except KeyError as e:
        print(f"Error: Missing key in JSON data - {e}")
    except Exception as e:
        print(f"Error: {e}")


# Function to retrieve all the invoiceid that are unpaid
def get_unpaid_invoices():
    try:
        # Connect to the database
        connection = sqlite3.connect("invoices.sqlite")
        cursor = connection.cursor()

        # Query for all UNPAID invoice IDs
        cursor.execute('''
        SELECT invoiceId FROM invoices WHERE state = 'UNPAID'
        ''')

        # Fetch all results
        result = cursor.fetchall()
        connection.close()

        if result:
            # Extract invoice IDs from the result tuples
            return [row[0] for row in result]
        else:
            return "No unpaid invoices found."
    except Exception as e:
        return f"Error: {e}"


# Function to retrieve all invoice IDs with state PAID and delivered set as NO
def get_paid_undelivered_invoices():
    try:
        # Connect to the database
        connection = sqlite3.connect("invoices.sqlite")
        cursor = connection.cursor()

        # Query for all invoice IDs where state is PAID and delivered is NO
        cursor.execute('''
        SELECT invoiceId FROM invoices 
        WHERE state = 'PAID' AND delivered = 'NO'
        ''')

        # Fetch all results
        result = cursor.fetchall()
        connection.close()

        if result:
            # Extract invoice IDs from the result tuples
            return [row[0] for row in result]
        else:
            return "No paid but undelivered invoices found."
    except Exception as e:
        return f"Error: {e}"


# Function to set delivered status to 'YES' for a given invoiceId
def set_invoice_delivered(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect("invoices.sqlite")
        cursor = connection.cursor()

        # Execute the UPDATE query to set delivered as 'YES'
        cursor.execute('''
        UPDATE invoices SET delivered = 'YES' WHERE invoiceId = ?
        ''', (invoice_id,))

        # Commit the changes
        connection.commit()
        affected_rows = cursor.rowcount
        connection.close()

        # Return the result
        if affected_rows > 0:
            return f"Invoice with ID {invoice_id} marked as delivered."
        else:
            return f"No invoice found with ID {invoice_id}."
    except Exception as e:
        return f"Error: {e}"


# Function to delete a row where the invoiceId matches. Good to clean the database of unpaid expired invoices
def delete_invoice_by_id(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect("invoices.sqlite")
        cursor = connection.cursor()

        # Execute the DELETE query
        cursor.execute('''
        DELETE FROM invoices WHERE invoiceId = ?
        ''', (invoice_id,))

        # Commit the changes
        connection.commit()
        affected_rows = cursor.rowcount
        connection.close()

        # Return the result
        if affected_rows > 0:
            return f"Invoice with ID {invoice_id} successfully deleted."
        else:
            return f"No invoice found with ID {invoice_id}."
    except Exception as e:
        return f"Error: {e}"


# Function to check if an invoiceId is still valid. Each invoice expires in 1 hour
def is_invoice_valid(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect("invoices.sqlite")
        cursor = connection.cursor()

        # Get the current time in ISO 8601 format
        current_time = datetime.utcnow().isoformat()

        # Query to check if the invoiceId is valid
        cursor.execute('''
        SELECT expiration FROM invoices 
        WHERE invoiceId = ? AND expiration > ?
        ''', (invoice_id, current_time))

        # Fetch the result
        result = cursor.fetchone()
        connection.close()

        # Check if a result was found
        if result:
            return True
        else:
            return False
    except Exception as e:
        return f"Error: {e}"
