# LNPay-Backend

LNPay-Backend is a backend solution for handling Bitcoin Lightning Network payments using the Strike API. It allows you to generate and manage Lightning invoices, track payment statuses, and handle delivery status, all while storing invoice data in a local SQLite database. This solution is ideal for e-commerce platforms.

## Introduction

This project was inspired by the lack of real-world applications for the Lightning Network in e-commerce. Many websites that accept Bitcoin as payment still rely on Layer 1, and some don’t even use native SegWit addresses, which increases transaction fees for customers, not to mention the slowness of Layer 1 transactions. In contrast, the Lightning Network is fast, highly scalable, and reliable. You don’t need to set up your own node or open channels with every client, simply use a good Lightning Network API like Strike. I'm not sponsored by them; I just really appreciate how well-documented their API is.

I developed this backend to simplify the integration of Bitcoin payments into e-commerce platforms. It’s incredibly easy to install, just download Python, install the dependencies, configure your .env file, and run main.py. That’s it!

You can read more about it below!

## Features

- **Invoice Generation**: Automatically generate Bitcoin Lightning invoices using the Strike API.
- **Currency to BTC Conversion**: Convert amounts in supported currencies to BTC using the CoinGecko API.
- **Invoice Management**: Store and manage invoice data in an SQLite database.
- **Payment Verification**: Verify the status of Lightning invoices (paid or unpaid).
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
   - Create a `.env` file in the `config directory`.
   - Add your Strike API key and any additional environment variables:
     ```env
     STRIKE_API_KEY=your_api_key_here
     WEBHOOK_SECRET=your_secret_to_sign_your_webhook
     WEBHOOK_URL=https://your-domain-for-the-webhook.com/webhook
     TIME_OFFSET=120 #time in seconds for the invoice expiration
     CURRENCY=usd #the currency your products are listed on your website so CoinGecko API can convert to Bitcoin
     ```
   - [How to obtain your Strike API key](https://docs.strike.me/).

## Usage

### 1. Running the Backend Server
To start the backend server, run:
```bash
python main.py
```
An `invoices.sqlite` file will be generated to store the invoices created by the user.

### 2. Generate an Invoice
Send a POST request to `/generate-invoice` with the desired amount:

Json:
```json
{
  "amount_fiat": "0.01",
  "ln_address": "customer_lightning_address_for_refunding_expired_invoice",
  "description": "Refund for order #12345",
  "correlation_id": "abc123xyz"
}
```

Curl:
```bash
curl -X POST http://localhost:5000/generate-invoice -H "Content-Type: application/json" -d "{\"amount_fiat\": \"0.01\", \"ln_address\": \"customerlightningaddressforrefundactions\", \"description\": \"Refund for order #12345\", \"correlation_id\": \"abc123xyz\"}"
```

This will return:
- Invoice details
- A QR code (Base64) for the Lightning invoice

### 3. Worker Scripts

- **`main_worker.py`**: Updates the status of unpaid invoices.
- **`expired_worker.py`**: Identifies expired invoices and processes automatic refunds.
- **`refund_failure_worker.py`**: Retries refunds that previously failed.

Schedule these scripts using Cron (Linux) or Task Scheduler (Windows) for continuous operation. Do not run `main_worker.py` together with your webhook, as they might conflict. You should run both `expired_worker.py` and `refund_failure_worker.py`, as they handle the task of refunding invoices that encountered errors for some reason.

### 4. Webhook Integration
**LNPay** supports webhook notifications to process payments and automatically update invoice statuses. (Your web server should also have a webhook set up to receive updates from **LNPay**).

#### Setting Up Webhooks
1. Configure your webhook URL as well as your secret in the Strike API by using `webhook_settings.py`

2. Update your `.env` :
   ```env
   WEBHOOK_URL=https://your-domain-for-the-webhook.com/webhook
   WEBHOOK_SECRET=your_webhook_secret_here
   ```

#### How Webhooks Work
- The webhook endpoint (`/webhook`) receives payment notifications from the Strike API.
- The `webhook_signature.py` verifies the authenticity of incoming requests using the `WEBHOOK_SECRET`.
- The `webhook_invoice.py` processes the payment and updates the database.

#### Testing Webhooks
You can use tools like [Cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) to expose your local server to the internet and test webhook functionality:

```bash
cloudflared-windows-amd64.exe tunnel --url http://127.0.0.1:5000
```

Copy the generated URL and set it as your webhook URL in the `.env` file.

```env
WEBHOOK_URL=https://your-domain-for-the-webhook.com/webhook
```

You can use `key_generator.py` to generate a random 10 length string to use as your webhook secret.

### 5. Customize Delivery Logic

Update `delivery.py` to incorporate your custom logic for handling invoice delivery. This is where **LNPay** will send a POST request to your webhook, notifying you when the payment is successful.

### 6. Test It Yourself

You can download [sampleSiteLNPay](https://github.com/ils94/sampleSiteLNPay) to test the capabilities of the backend. Simply download both **LNPay-Backend** and **sampleSiteLNPay**, run both servers, and test them by sending small amounts of Bitcoin.

## Troubleshooting

- **Strike API Connection Issues**: Ensure your API key is valid and the Strike API is reachable.
- **Database Errors**: Verify that the SQLite database file (`invoices.sqlite`) exists and is writable.
- **Worker Scripts Not Running**: Check your task scheduler or cron job configuration.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For further questions or support, refer to the [Strike API documentation](https://docs.strike.me/) or open an issue on this repository.


