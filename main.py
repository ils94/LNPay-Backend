from flask import Flask, request, jsonify
import invoice
import qrcodeimage
import db

app = Flask(__name__)


# Main endpoint for the backend. This will generate the invoice after receiving an amount
@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    try:
        # Extract the amount or other data from the request if needed
        data = request.get_json()
        amount = data.get("amount")

        # Call the generate function.
        invoice_json = invoice.generate(amount)

        # Generate a QR code for the invoice
        qr_code_image_base64 = qrcodeimage.generate(invoice_json['quote']['lnInvoice'])

        # Create the final response JSON
        response_data = {
            "status": "success",
            "data": {
                "invoice": invoice_json["invoice"],
                "quote": invoice_json["quote"],
                "qr_code": qr_code_image_base64
            }
        }

        # Insert the relevant data of the invoice into a database for future use
        db.insert_invoice(response_data)

        # Return the JSON response
        return jsonify(response_data), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    db.create_database()

    app.run(debug=True)
