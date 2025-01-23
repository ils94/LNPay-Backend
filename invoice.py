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
