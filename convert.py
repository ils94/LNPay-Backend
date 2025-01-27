import requests
import currencies
import time

# Variable to store the last fetch time and price
# Had to do it, since it is so easy to reach the api limit of CoinGecko
last_fetch_time = 0
cached_btc_price = None


# Function to convert fiat into BTC using CoinGecko API
def fiat_to_btc(amount, currency):
    global last_fetch_time, cached_btc_price

    # Ensure the currency exists in the fiat dictionary
    if currency not in currencies.fiat:
        raise ValueError(
            f"Currency '{currency}' is not supported. Please choose from: {', '.join(currencies.fiat.keys())}")

    current_time = time.time()

    # Check if 1:30 minutes (90 seconds) have passed since the last fetch
    if current_time - last_fetch_time > 90 or cached_btc_price is None:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}"
        response = requests.get(url)
        data = response.json()

        # Get the current BTC to specified currency exchange rate
        cached_btc_price = data['bitcoin'][currency]
        last_fetch_time = current_time  # Update the last fetch time

    # Convert the specified currency amount to BTC
    btc_amount = amount / cached_btc_price

    # Format the result with 8 decimal places
    return round(btc_amount, 8)
