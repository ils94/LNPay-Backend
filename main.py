from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Strike API Configuration
STRIKE_API_BASE_URL = "https://api.strike.me/v1"
STRIKE_API_KEY = os.getenv("STRIKE_API_KEY")


@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        amount = data.get("amount")

        if not amount:
            return jsonify({"error": "Amount is required"}), 400

        # Prepare request payload
        payload = {
            "amount": amount,
            "currency": "BTC"
        }

        # Strike API headers
        headers = {
            "Authorization": f"Bearer {STRIKE_API_KEY}",
            "Content-Type": "application/json"
        }

        # Call the Strike API to create an invoice
        response = requests.post(f"{STRIKE_API_BASE_URL}/invoices", json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 201:
            # Return the Lightning invoice to the client
            return jsonify({"invoice": response_data}), 201
        else:
            # Log and return errors from the Strike API
            print("Strike API response:", response_data)
            return jsonify({"error": response_data.get("message", "Unknown error")}), response.status_code

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
