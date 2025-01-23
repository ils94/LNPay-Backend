import requests
import currencies


# Function to convert fiat into BTC using CoinGecko API
# Not all fiat currency is compatible
def fiat_to_btc(amount, currency):
    # Ensure the currency exists in the fiat dictionary
    if currency not in currencies.fiat:
        raise ValueError(
            f"Currency '{currency}' is not supported. Please choose from: {', '.join(currencies.fiat.keys())}")

    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}"
    response = requests.get(url)
    data = response.json()

    # Get the current BTC to specified currency exchange rate
    btc_price_in_currency = data['bitcoin'][currency]

    # Convert the specified currency amount to BTC
    btc_amount = amount / btc_price_in_currency

    # Format the result with 8 decimal places
    return round(btc_amount, 8)
