import requests
import globalvariables


# Function to call the Strike API to check an invoice state (paid or unpaid)
def paid_invoice(invoice_id):
    invoice_url = f'{globalvariables.base_url}/invoices/{invoice_id}'

    headers = {
        'Authorization': f'Bearer {globalvariables.api_key}',
        'accept': 'application/json'
    }

    response = requests.get(invoice_url, headers=headers)

    # If success, return either paid or unpaid
    if response.status_code == 200:
        invoice = response.json()
        return invoice['state']
    else:
        raise Exception(response.json())
