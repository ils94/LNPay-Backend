from flask import Flask, request, jsonify
import generate

app = Flask(__name__)


@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    try:
        # Extract the amount or other data from the request if needed
        data = request.get_json()
        amount = data.get("amount", 449.95)  # Default to Unlimited Wraith Cannon if no amount is provided

        # Call the generate function
        invoice = generate.invoice(amount)

        # Return a success response
        return jsonify({"status": "success", "invoice": invoice}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
