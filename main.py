from flask import Flask, request, jsonify
import invoice
import qrcodeimage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    try:
        # Extract the amount or other data from the request if needed
        data = request.get_json()
        amount = data.get("amount", 449.95)  # Default to Unlimited Wraith Cannon if no amount is provided

        # Call the generate function
        invoice_json = invoice.generate(amount, "test")

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

        # Return the JSON response
        return jsonify(response_data), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
