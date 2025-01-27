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
import global_variables


# Functions to execute refunds
# There is not a refund endpoint for Strike API, so what I did was basically create a payment to the user
# to send back what he/she sent when the invoices were considered expired by the server's worker
# It a gimmick, but works
def create_payment_quote(lightning_address, amount):
    """
    Create a payment quote for a Lightning Address.
    """

    headers = {
        "Authorization": f"Bearer {global_variables.api_key}",
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
        "description": "Refunded for a due expired invoice"  # Note for the user
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
        "Authorization": f"Bearer {global_variables.api_key}",
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
