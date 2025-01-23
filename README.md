# LNPay-Backend

LNPay-Backend is a backend solution for handling Bitcoin Lightning Network payments using the Strike API. It allows you to generate and manage Lightning invoices, track payment statuses, and handle delivery status, all while storing invoice data in a local SQLite database.

## Features

- **Invoice Generation**: Automatically generate Bitcoin Lightning invoices using the Strike API.
- **USD to BTC Conversion**: Convert amounts in USD to BTC using the CoinGecko API.
- **Invoice Management**: Store and manage invoice data in an SQLite database.
- **Payment Verification**: Verify the status of Lightning invoices (paid or unpaid).
- **Automated Status Updates**: Use a worker script to loop through and update invoice statuses and delivery status.
- **QR Code Generation**: Generate QR codes for Lightning invoices for easy payment.

## Requirements

- Python 3.7+
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
   - Add your Strike API key:
     ```env
     STRIKE_API_KEY=your_api_key_here
     ```

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
1. Run the `worker.py` script:
   ```bash
   python worker.py
   ```
   The worker script:
   - Loops through all unpaid invoices.
   - Checks their status using the Strike API.
   - Updates the status in the database.

### 3. Generate an Invoice
Send a POST request to `/generate-invoice` with the desired amount:
```json
{
  "amount": 0.01
}
```
Curl
```
curl -X POST http://localhost:5000/generate-invoice -H "Content-Type: application/json" -d "{\"amount\": 0.01}"
```
This will return:
- Invoice details
- A QR code (Base64) for the Lightning invoice

### 4. Manage Invoices
The following utility functions are available for managing invoices:
- **Get unpaid invoices**
- **Mark invoices as paid**
- **Mark invoices as delivered**
- **Delete unpaid but expired invoices**

## File Structure

```
LNBackEnd/
├── main.py             # Main Flask application
├── worker.py           # Worker script to check and update invoice statuses
├── db.py               # SQLite database setup and queries
├── invoice.py          # Invoice generation and management
├── qrcodeimage.py      # QR code generation
├── metadata.py         # Helper functions for metadata generation
├── convert.py          # USD to BTC conversion logic
├── checkstatus.py      # Strike API integration for status checks
├── templates/
│   └── qr_code.html    # HTML template for displaying QR codes
├── .env                # Environment variables (not included in repo)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Notes

- The `worker.py` script should be run alongside the Flask server to continuously update invoice statuses.
- The database (`invoices.sqlite`) is created automatically if it does not exist when running `main.py`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
