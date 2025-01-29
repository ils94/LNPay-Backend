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

import sqlite3
from datetime import datetime, timedelta
from src.config import global_variables
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "invoices.sqlite")


# Function to create the SQLite database and table
def create_database():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount TEXT,
        currency TEXT,
        correlation TEXT,
        created TEXT,
        description TEXT,
        invoiceId TEXT,
        state TEXT,
        delivered TEXT,
        expiration TEXT,
        lnInvoice TEXT,
        refund_address TEXT
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expired (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount TEXT,
            currency TEXT,
            correlation TEXT,
            created TEXT,
            description TEXT,
            invoiceId TEXT,
            state TEXT,
            delivered TEXT,
            expiration TEXT,
            lnInvoice TEXT,
            refund_address TEXT
        )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS refund_failure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount TEXT,
                currency TEXT,
                correlation TEXT,
                created TEXT,
                description TEXT,
                invoiceId TEXT,
                state TEXT,
                delivered TEXT,
                expiration TEXT,
                lnInvoice TEXT,
                refund_address TEXT
            )
            ''')
    connection.commit()
    connection.close()


# Function to insert data into the SQLite database
def insert_invoice(json_data, ln_address):
    # Extract relevant information from the JSON
    try:

        invoice = json_data['data']['invoice']
        quote = json_data['data']['quote']

        amount = invoice['amount']['amount']
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
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO invoices (
            amount, currency, correlation, created, description, 
            invoiceId, state, delivered, expiration, lnInvoice, refund_address
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (amount, currency, correlation, created, description,
              invoiceid, state, delivered, expiration, lninvoice, ln_address))

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
        connection = sqlite3.connect(db_path)
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
    except Exception as e:
        return f"Error: {e}"


# Function to check if a given invoice ID has the state 'PAID'
def is_invoice_paid(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to check if the invoice state is 'PAID' for the given invoice ID
        cursor.execute('''SELECT state FROM invoices WHERE invoiceId = ?''', (invoice_id,))

        # Fetch the result
        result = cursor.fetchone()
        connection.close()

        if result:
            # If the result is found, return if the state is 'PAID'
            if result[0] == 'PAID':
                return True
            else:
                return False
        else:
            # If no invoice with that ID is found
            return False

    except Exception as e:
        return f"Error: {e}"


# Function to set the state of an invoice to 'PAID'
def set_invoice_paid(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Execute the UPDATE query to set state as 'PAID'
        cursor.execute('''
        UPDATE invoices SET state = 'PAID' WHERE invoiceId = ?
        ''', (invoice_id,))

        # Commit the changes
        connection.commit()
        affected_rows = cursor.rowcount
        connection.close()

        # Return the result
        if affected_rows > 0:
            return f"Invoice with ID {invoice_id} marked as paid."
    except Exception as e:
        return f"Error: {e}"


# Function to retrieve all invoice IDs with state PAID and delivered set as NO
def get_paid_undelivered_invoices():
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
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
        connection = sqlite3.connect(db_path)
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
    except Exception as e:
        return f"Error: {e}"


# Function to get the 'delivered' status of an invoice
def get_delivered_status(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to get the delivered status of the given invoiceId
        cursor.execute('''
        SELECT delivered FROM invoices WHERE invoiceId = ?
        ''', (invoice_id,))

        # Fetch the result
        result = cursor.fetchone()
        connection.close()

        if result:
            # Return the delivered status (should be "YES" or "NO")
            return result[0]
    except Exception as e:
        return f"Error: {e}"


# Function to delete a row where the invoiceId matches. Good to clean the database of unpaid expired invoices
def delete_invoice_by_id(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
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
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Get the current time in ISO 8601 format
        current_time = (datetime.utcnow() + timedelta(minutes=global_variables.expiration_offset)).strftime(
            '%Y-%m-%dT%H:%M:%SZ')

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


# Function to check if an invoiceId is still valid. Each invoice expires in 1 hour
def is_invoice_valid_one_hour(invoice_id):
    try:

        # Add more time to make sure
        offset_minutes = -5

        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Get the current time in ISO 8601 format
        current_time = (datetime.utcnow() + timedelta(minutes=offset_minutes)).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Query to check if the invoiceId is valid
        cursor.execute('''
        SELECT expiration FROM expired 
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


def get_refund_details(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to get refund_address and amount from refund_failure table for the given invoiceId
        cursor.execute('''
        SELECT refund_address, amount FROM invoices WHERE invoiceId = ?
        ''', (invoice_id,))

        # Fetch the result
        result = cursor.fetchone()
        connection.close()

        if result:
            # Return both refund_address and amount as a tuple
            return result[0], result[1]
        else:
            # Explicitly return None to handle no results
            return None, None

    except Exception as e:
        return f"Error: {e}"


# Function to copy a row to the expired table based on invoiceId
def copy_to_expired(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Select the row where invoiceId matches
        cursor.execute('''
        SELECT amount, currency, correlation, created, description, invoiceId, 
               state, delivered, expiration, lnInvoice, refund_address
        FROM invoices WHERE invoiceId = ?
        ''', (invoice_id,))
        row = cursor.fetchone()

        if row:
            # Insert the row into the expired table
            cursor.execute('''
            INSERT INTO expired (
                amount, currency, correlation, created, description, invoiceId, 
                state, delivered, expiration, lnInvoice, refund_address
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)

            # Commit the changes
            connection.commit()
            connection.close()

            return f"Invoice with ID {invoice_id} copied to the expired table."
        else:
            connection.close()
            return f"No invoice found with ID {invoice_id}."
    except Exception as e:
        return f"Error: {e}"


# Function to select all records from the expired table
def get_all_expired():
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to select all records from the expired table
        cursor.execute('''
        SELECT * FROM expired
        ''')

        # Fetch all results
        result = cursor.fetchall()
        connection.close()

        if result:
            # Extract column 6 from all rows
            column_6_values = [row[6] for row in result]
            return column_6_values
        else:
            return []  # Return an empty list if no rows found
    except Exception as e:
        return f"Error: {e}"


# Function to retrieve refund_address and amount from the expired table based on invoiceId
def get_expired_details(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to get refund_address and amount from expired table for the given invoiceId
        cursor.execute('''
        SELECT refund_address, amount FROM expired WHERE invoiceId = ?
        ''', (invoice_id,))

        # Fetch the result
        result = cursor.fetchone()
        connection.close()

        if result:
            # Return both refund_address and amount as a tuple
            return result[0], result[1]
        else:
            # Explicitly return None to handle no results
            return None, None

    except Exception as e:
        return f"Error: {e}", None


# Function to delete a row where the invoiceId matches. Good to clean the database of unpaid expired invoices
def delete_expired_invoice(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Execute the DELETE query
        cursor.execute('''
        DELETE FROM expired WHERE invoiceId = ?
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


# Function to copy a row to the refund_failure table based on invoiceId
# You can run a refund again using only this table if necessary
def copy_to_refund_failure(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Select the row where invoiceId matches
        cursor.execute('''
        SELECT amount, currency, correlation, created, description, invoiceId, 
               state, delivered, expiration, lnInvoice, refund_address
        FROM invoices WHERE invoiceId = ?
        ''', (invoice_id,))
        row = cursor.fetchone()

        if row:
            # Insert the row into the expired table
            cursor.execute('''
            INSERT INTO refund_failure (
                amount, currency, correlation, created, description, invoiceId, 
                state, delivered, expiration, lnInvoice, refund_address
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)

            # Commit the changes
            connection.commit()
            connection.close()

            return f"Invoice with ID {invoice_id} copied to the expired table."
        else:
            connection.close()
            return f"No invoice found with ID {invoice_id}."
    except Exception as e:
        return f"Error: {e}"


# Function to retrieve refund_address and amount from the refund_failure table based on invoiceId
def get_refund_failure_details(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to get refund_address and amount from refund_failure table for the given invoiceId
        cursor.execute('''
        SELECT refund_address, amount FROM refund_failure WHERE invoiceId = ?
        ''', (invoice_id,))

        # Fetch the result
        result = cursor.fetchone()
        connection.close()

        if result:
            # Return both refund_address and amount as a tuple
            return result[0], result[1]
        else:
            # Explicitly return None to handle no results
            return None, None

    except Exception as e:
        return f"Error: {e}"


# Function to select all records from the refund_failure table
def get_all_refund_failures():
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to select all records from the expired table
        cursor.execute('''
        SELECT * FROM refund_failure
        ''')

        # Fetch all results
        result = cursor.fetchall()
        connection.close()

        if result:
            # Extract column 6 from all rows
            column_6_values = [row[6] for row in result]
            return column_6_values
        else:
            return []  # Return an empty list if no rows found
    except Exception as e:
        return f"Error: {e}"


# Function to delete a row where the invoiceId matches. Good to clean the database of unpaid expired invoices
def delete_refund_failure_invoice(invoice_id):
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Execute the DELETE query
        cursor.execute('''
        DELETE FROM refund_failure WHERE invoiceId = ?
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
