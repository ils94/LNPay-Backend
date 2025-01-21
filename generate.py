import requests
import datetime
import os
from dotenv import load_dotenv
import convert


def invoice(usd):
    # Load env to get the api key
    load_dotenv()

    STRIKE_API_BASE_URL = "https://api.strike.me/v1"
    STRIKE_API_KEY = os.getenv("STRIKE_API_KEY")

    # Convert the amount in USD to BTC
    btc_amount = convert.usd_to_btc(float(usd))

    if not btc_amount:
        raise Exception('Error converting USD to BTC')

    # Get current system time to generate a unique ID for the transaction
    now = datetime.datetime.now()
    transaction_id = now.strftime('%d%m%Y%H%M%S') + f'{now.microsecond // 10000}{(now.microsecond % 10000) // 100}'

    # Generate the invoice using the API endpoints
    invoice_endpoint = f'{STRIKE_API_BASE_URL}/invoices'
    quote_endpoint = f'{invoice_endpoint}/{{invoice_id}}/quote'

    invoice_data = {
        'correlationId': f'{transaction_id}',
        'description': f'Transaction ID: {transaction_id}',
        'amount': {
            'currency': 'BTC',
            'amount': str(btc_amount)
        }
    }

    headers = {
        'Authorization': f'Bearer {STRIKE_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Receive the invoice_response
    invoice_response = requests.post(invoice_endpoint, json=invoice_data, headers=headers)

    if invoice_response.status_code == 201:

        invoice = invoice_response.json()
        invoice_id = invoice['invoiceId']

        quote_url = quote_endpoint.format(invoice_id=invoice_id)
        quote_response = requests.post(quote_url, headers=headers)

        if quote_response.status_code == 201:

            quote = quote_response.json()

            # Return the invoice, description, amount (can add more stuff here if you want)
            return quote['lnInvoice'], quote['description'], quote['targetAmount']['amount']
        else:
            raise Exception(quote_response.json())
    else:
        raise Exception(invoice_response.json())
