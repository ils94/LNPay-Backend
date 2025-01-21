import requests
import datetime
import os
from dotenv import load_dotenv
import usd_to_btc


def gerar_invoice(usd):
    load_dotenv()

    STRIKE_API_BASE_URL = "https://api.strike.me/v1"
    STRIKE_API_KEY = os.getenv("STRIKE_API_KEY")

    btc_amount = usd_to_btc.usd_to_btc(float(usd))

    if not btc_amount:
        raise Exception('Error converting USD to BTC')

    now = datetime.datetime.now()

    formatted_time = now.strftime('%d%m%Y%H%M%S') + f'{now.microsecond // 10000}{(now.microsecond % 10000) // 100}'

    invoice_endpoint = f'{STRIKE_API_BASE_URL}/invoices'
    quote_endpoint = f'{invoice_endpoint}/{{invoice_id}}/quote'

    invoice_data = {
        'correlationId': f'{formatted_time}',
        'description': f'Transaction ID: {formatted_time}',
        'amount': {
            'currency': 'BTC',
            'amount': str(btc_amount)
        }
    }

    headers = {
        'Authorization': f'Bearer {STRIKE_API_KEY}',
        'Content-Type': 'application/json'
    }

    invoice_response = requests.post(invoice_endpoint, json=invoice_data, headers=headers)

    if invoice_response.status_code == 201:

        invoice = invoice_response.json()
        invoice_id = invoice['invoiceId']

        quote_url = quote_endpoint.format(invoice_id=invoice_id)
        quote_response = requests.post(quote_url, headers=headers)

        if quote_response.status_code == 201:

            quote = quote_response.json()

            print(quote['lnInvoice'])

            return quote['lnInvoice'], quote['description'], quote['targetAmount']['amount']
        else:
            raise Exception(quote_response.json())
    else:
        raise Exception(invoice_response.json())



gerar_invoice(499)
