import os
from dotenv import load_dotenv

# Load the .env to retrieve your API Key
load_dotenv()

base_url = "https://api.strike.me/v1"
api_key = os.getenv("STRIKE_API_KEY")

currency = "usd"

expiration_offset = 45
