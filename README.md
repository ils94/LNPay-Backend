# LNPay-Backend

LNPay-Backend is a backend solution for handling Bitcoin Lightning Network payments using the Strike API. It allows you to generate and manage Lightning invoices, track payment statuses, and handle delivery status, all while storing invoice data in a local SQLite database. This solution is ideal for e-commerce platforms.

## Features

- **Invoice Generation**: Automatically generate Bitcoin Lightning invoices using the Strike API.
- **Currency to BTC Conversion**: Convert amounts in supported currencies to BTC using the CoinGecko API.
- **Invoice Management**: Store and manage invoice data in an SQLite database.
- **Payment Verification**: Verify the status of Lightning invoices (paid or unpaid).
- **Automated Status Updates**: Use worker scripts to update invoice statuses and delivery status.
- **QR Code Generation**: Generate QR codes for Lightning invoices for easy payment.
- **Automatic Refunds**: Refund expired invoices automatically.
- **Webhook Integration**: Handle payment notifications via webhooks.
- **Webhook Subscription Management**: Subscribe, unsubscribe, update, and list your webhooks.

## Requirements

- Python 3.9+ (because of Async)
- SQLite (included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ils94/LNPay-Backend.git
   cd LNPay-Backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add your Strike API key and any additional environment variables:
     ```env
     STRIKE_API_KEY=your_api_key_here
     ```
   - [How to obtain your Strike API key](https://docs.strike.me/).

## Usage

### 1. Running the Backend Server
To start the backend server, run:
```bash
python main.py
```
This will:
- Automatically create the SQLite database (`invoices.sqlite`) if it does not already exist.
- Start the Flask application for generating invoices and serving QR codes.

### 2. Verifying Invoice Status
To verify the status of invoices and update the database:
1. Run the `main_worker.py` script:
   ```bash
   python main_worker.py
   ```
   The worker script:
   - Loops through all unpaid invoices.
   - Checks their status using the Strike API.
   - Updates the status in the database.

> **Note**: If you plan to use webhooks, it is recommended not to use the `main_worker.py` script. Relying on webhooks will delegate state updates to Strike, which can simplify your workflow but introduces dependency on their notifications.

### 3. Generate an Invoice
Send a POST request to `/generate-invoice` with the desired amount:
```json
{
  "amount": 0.01,
  "ln_address": "customerlightningaddressforrefundactions"
}
```
Curl:
```bash
curl -X POST http://localhost:5000/generate-invoice \
     -H "Content-Type: application/json" \
     -d "{\"amount\": 0.01, \"ln_address\": \"customerlightningaddressforrefundactions\"}" \
     > "%USERPROFILE%\Desktop\response.html"
```
This will return:
- Invoice details
- A QR code (Base64) for the Lightning invoice

### 4. Worker Scripts

- **`main_worker.py`**: Updates the status of unpaid invoices.
- **`expired_worker.py`**: Identifies expired invoices and processes automatic refunds.
- **`refund_failure_worker.py`**: Retries refunds that previously failed.

Schedule these scripts using cron (Linux) or Task Scheduler (Windows) for continuous operation.

### 5. Webhook Integration
LNPay-Backend supports webhook notifications to process payments and update invoice statuses automatically.

#### Setting Up Webhooks
1. Configure your webhook URL in the Strike API dashboard. Use the following format:
   ```
   http://<your_server_address>/webhook
   ```

2. Update your `.env` file with the required secret for verifying webhook signatures:
   ```env
   WEBHOOK_SECRET=your_webhook_secret_here
   ```

3. Start the Flask server (`main.py`) to listen for incoming webhook events.

#### How Webhooks Work
- The webhook endpoint (`/webhook`) receives payment notifications from the Strike API.
- The `webhook_signature.py` verifies the authenticity of incoming requests using the `WEBHOOK_SECRET`.
- The `webhook_invoice.py` processes the payment and updates the database.

#### Testing Webhooks
You can use tools like [Cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) to expose your local server to the internet and test webhook functionality:

cloudflared:

```bash
cloudflared-windows-amd64.exe tunnel --url http://127.0.0.1:5000
```

Copy the generated URL and set it as your webhook URL in the `.env` file.

```env
WEBHOOK_URL=https://yoururlhere/webhook
```

### 6. Webhook Subscription Management
The `webhook_subscription.py` module includes functions to:

- **Subscribe to a webhook**: Create a new webhook subscription.
- **Unsubscribe from a webhook**: Remove an existing webhook subscription.
- **Update a webhook**: Modify an existing subscription.
- **List subscriptions**: View all current webhook subscriptions.

You can use these functions programmatically by importing the module into your scripts. Refer to the code in `webhook_subscription.py` for usage examples.

You can use `key_generator.py` to generate a random 10 length string to use as your webhook secret.

### 7. Customize Delivery Logic
Update `delivery.py` to include your custom logic for handling invoice delivery.

## File Structure

```
LNPay-Backend/
├── .env                      # Environment variables (not included in repo)
├── LICENSE                   # MIT
├── README.md                 # Project documentation
├── checkstatus.py            # Strike API integration for status checks
├── convert.py                # Currency to BTC conversion logic
├── currencies.py             # Supported currencies from CoinGecko
├── db.py                     # SQLite database setup and queries
├── delivery.py               # Custom logic for invoice delivery
├── expired_worker.py         # Worker script to check expired invoices and refund them
├── global_variables.py       # Global variables for the project
├── invoice.py                # Invoice generation and management
├── key_generator.py          # Generate a random 10+ length key to use as your webhook secret
├── main.py                   # Main Flask application
├── main_worker.py            # Worker script to update invoice statuses
├── metadata.py               # Metadata generation helpers
├── qr_code_generator.py      # QR code generation logic
├── refund_api.py             # Functions for initiating refunds
├── refund_failure_worker.py  # Worker script to retry refund attempts
├── requirements.txt          # Python dependencies
├── webhook_invoice.py        # Logic to process payments via webhook
├── webhook_signature.py      # Verifies webhook signatures
├── webhook_subscription.py   # Webhook subscription management
└── templates/
    └── qr_code.html          # HTML template for displaying QR codes
```

## Notes

- The `main_worker.py` script should be run alongside the Flask server to continuously update invoice statuses unless you are relying solely on webhooks.
- The database (`invoices.sqlite`) is created automatically if it does not exist when running `main.py`.
- Secure your `.env` file and restrict database access in production.

## Troubleshooting

- **Strike API Connection Issues**: Ensure your API key is valid and the Strike API is reachable.
- **Database Errors**: Verify that the SQLite database file (`invoices.sqlite`) exists and is writable.
- **Worker Scripts Not Running**: Check your task scheduler or cron job configuration.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For further questions or support, refer to the [Strike API documentation](https://docs.strike.me/) or open an issue on this repository.

