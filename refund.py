import requests
import globalvariables


# Functions to execute refunds
# There is not a refund endpoint for Strike API, so what I did was basically create a payment to the user
# to send back what he/she sent when the invoices were considered expired by the server's worker
# It a gimmick, but works
def create_payment_quote(lightning_address, amount):
    """
    Create a payment quote for a Lightning Address.
    """

    headers = {
        "Authorization": f"Bearer {globalvariables.api_key}",
        "Content-Type": "application/json"
    }

    url = "https://api.strike.me/v1/payment-quotes/lightning/lnurl"  # Correct endpoint

    data = {
        "lnAddressOrUrl": lightning_address,
        "sourceCurrency": "BTC",
        "amount": {
            "amount": str(amount),
            "currency": "BTC"
        },
        "description": "Refund for expired invoice"  # Note for the user
    }

    response = requests.post(url, json=data, headers=headers)

    print(f"response: {response}")

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None


def execute_payment(quote_id):
    """
    Execute the payment using the generated payment quote ID.
    """

    url = f"https://api.strike.me/v1/payment-quotes/{quote_id}/execute"

    headers = {
        "Authorization": f"Bearer {globalvariables.api_key}",
        "Accept": "application/json"
    }

    response = requests.patch(url, headers=headers)

    print(f"response: {response}")

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None


def is_success(lightning_address, amount):
    # Step 1: Create a payment quote
    quote_response = create_payment_quote(lightning_address, amount)

    if quote_response and "paymentQuoteId" in quote_response:
        payment_quote_id = quote_response["paymentQuoteId"]

        # Step 2: Execute the payment
        execution_response = execute_payment(payment_quote_id)

        print("Payment Execution Response:", execution_response)

        if execution_response:
            return True
        else:
            return False
    else:
        print("Failed to create payment quote:", quote_response)
        return False
