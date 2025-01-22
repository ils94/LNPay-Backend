import sqlite3


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
        expiration = quote['expiration']
        lninvoice = quote['lnInvoice']

        # Insert into the database
        connection = sqlite3.connect("invoices.sqlite")
        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO invoices (
            amount, currency, correlation, created, description, 
            invoiceId, state, expiration, lnInvoice
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (amount, currency, correlation, created, description,
              invoiceid, state, expiration, lninvoice))

        connection.commit()
        connection.close()
        print("Invoice data inserted successfully.")
    except KeyError as e:
        print(f"Error: Missing key in JSON data - {e}")
    except Exception as e:
        print(f"Error: {e}")
