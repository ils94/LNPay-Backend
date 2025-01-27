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

import requests
import convert
import globalvariables
import metadata


# Function to generate an invoice. You can modify the part for the correlation id for something else that your system
# generates. It MUST be unique everytime, otherwise the Strike API will return an error (using the machine time with
# milliseconds was the best approach I came with)
def generate(amount):
    # Convert the amount in USD to BTC
    btc_amount = convert.fiat_to_btc(float(amount), globalvariables.currency)

    if not btc_amount:
        raise Exception(f'Error converting {globalvariables.currency} to BTC')

    correlation_id = metadata.generate_correlation_id()
    description = metadata.generate_description()

    # Generate the invoice using the API endpoints
    invoice_endpoint = f'{globalvariables.base_url}/invoices'
    quote_endpoint = f'{invoice_endpoint}/{{invoice_id}}/quote'

    invoice_data = {
        'correlationId': f'{correlation_id}',
        'description': f'{description}',
        'amount': {
            'currency': 'BTC',
            'amount': str(btc_amount)
        }
    }

    headers = {
        'Authorization': f'Bearer {globalvariables.api_key}',
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

            # Combine invoice and quote information into a single JSON object
            combined_response = {
                "invoice": invoice,
                "quote": quote
            }

            return combined_response
        else:
            raise Exception(quote_response.json())
    else:
        raise Exception(invoice_response.json())
