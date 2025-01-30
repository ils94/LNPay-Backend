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


import aiohttp


# Your website's server should have a webhook to communicate
async def send_webhook(data):
    url = 'http://localhost:8000/webhook'  # The Flask webhook URL

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                print("Webhook sent successfully!")
            else:
                print(f"Failed to send webhook, status code: {response.status}")


async def logic(invoice):

    ##############################
    #                            #
    #  Your logic when the       #
    #  payment is done           #
    #                            #
    ##############################

    print("Product/Service was delivered!")

    # Send success status to the webhook
    webhook_data = {
        "status": "success",
        "message": "Payment processed successfully!",
        "invoice": invoice
    }

    # Send the success message to the webhook
    await send_webhook(webhook_data)
