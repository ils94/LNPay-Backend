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
import json
import global_variables


# To be able to receive POST on your webhook from Strike API, you have to run this function first
# (just one time of course)
def subscribe():
    url = "https://api.strike.me/v1/subscriptions"

    payload = json.dumps({
        "webhookUrl": global_variables.webhook_url,  # Your Flask webhook URL
        "webhookVersion": "v1",
        "secret": global_variables.webhook_secret,  # Shared secret for signature validation
        "enabled": True,
        "eventTypes": [
            "invoice.updated"  # Only subscribe to invoice.updated events
        ]
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Bearer {global_variables.api_key}"  # Add your API token here
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Use this function to unsub by providing a subscription_id
def unsubscribe(subscription_id):
    # Replace these values with your actual API token and subscription ID
    api_token = global_variables.api_key

    # API endpoint for deleting a subscription
    url = f"https://api.strike.me/v1/subscriptions/{subscription_id}"

    # Headers for authorization
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    # Make the DELETE request
    response = requests.delete(url, headers=headers)

    # Print the response
    if response.status_code == 204:
        print("Subscription successfully deleted.")
    else:
        print(f"Failed to delete subscription: {response.status_code}")
        print(response.text)


# Use this function to list all activate subs
def list_subscriptions():
    # API endpoint for listing subscriptions
    url = "https://api.strike.me/v1/subscriptions"

    # Headers for authorization
    headers = {
        "Authorization": f"Bearer {global_variables.api_key}",
        "Accept": "application/json"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Print the response
    if response.status_code == 200:
        subscriptions = response.json()  # Parse JSON response
        for sub in subscriptions:
            print(f"ID: {sub['id']}")
            print(f"Webhook URL: {sub['webhookUrl']}")
            print(f"Event Types: {sub['eventTypes']}")
            print(f"Enabled: {sub['enabled']}")
            print("-" * 40)
    else:
        print(f"Failed to fetch subscriptions: {response.status_code}")
        print(response.text)
