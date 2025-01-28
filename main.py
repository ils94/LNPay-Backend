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

from flask import Flask, request, jsonify, render_template

import global_variables
import invoice
import qr_code_generator
import db
import webhook_signature
import asyncio
import webhook_invoice

app = Flask(__name__)


# Main endpoint for the backend. This will generate the invoice after receiving an amount
@app.route('/generate-invoice', methods=['POST'])
async def generate_invoice():
    try:
        # Extract the amount or other data from the request if needed
        data = request.get_json()
        amount = data.get("amount")
        ln_address = data.get("ln_address")

        # Call the generate function.
        invoice_json = await asyncio.to_thread(invoice.generate, amount)

        # Generate a QR code for the invoice
        qr_code_image_base64 = await asyncio.to_thread(qr_code_generator.generate, invoice_json['quote']['lnInvoice'])

        time = 60 - global_variables.expiration_offset

        # Create the final response JSON
        response_data = {
            "status": "success",
            "data": {
                "invoice": invoice_json["invoice"],
                "quote": invoice_json["quote"],
                "qr_code": qr_code_image_base64,
                "expiration_time": time
            }
        }

        # Insert the relevant data of the invoice into a database for future use
        await asyncio.to_thread(db.insert_invoice, response_data, ln_address)

        # Here you can choose what type of data you want to return

        # The response_data contains all the information of both invoice json and quote json as well as the qr code
        # base64. the render_template returns a qr_code.html containing the qr code to be scanned, the value in BTC
        # and the invoice string (for manual pasting into the app to send the BTC).

        # Return the JSON response
        # return jsonify(response_data), 200

        return render_template('qr_code.html', time=time, amount_sats=invoice_json['quote']['sourceAmount']['amount'],
                               qr_code=qr_code_image_base64, invoice=invoice_json['quote']['lnInvoice'])

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# A public server is required to test this.

# The webhook will notify you when an invoice's state changes. This is considered best practice
# compared to using main_worker.py.
# However, it relies on Strike consistently notifying you of invoice changes.
# Additionally, you are still limited by the number of API calls you make, as the webhook
# does not provide detailed information about invoice state changes (e.g., paid/unpaid).
# You will still need to use check_status.py to determine the actual state of the invoice.

@app.route('/webhook', methods=['POST'])
async def strike_webhook():
    """
    Endpoint to handle "invoice.updated" events from Strike.
    """
    try:
        # Get the raw request body
        raw_data = request.get_data()

        # Get the signature from the headers
        signature = request.headers.get('X-Webhook-Signature', '').upper()

        # Verify the signature
        if not webhook_signature.verify_request_signature(raw_data, signature, global_variables.webhook_secret):
            print("Signature verify error...")
            return jsonify({'error': 'Invalid signature'}), 400

        # Parse the JSON payload
        event_data = request.json

        # Only handle "invoice.updated" events
        if event_data.get('eventType') == 'invoice.updated':

            entity_id = event_data.get('data', {}).get('entityId')

            # start the invoice processing
            await webhook_invoice.check_state(entity_id)

            return jsonify({'status': 'success'}), 200

        # Ignore other events
        return jsonify({'message': 'Event ignored'}), 200

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({'error': 'Webhook handling failed'}), 500


if __name__ == '__main__':
    db.create_database()

    app.run(debug=True)
