import requests


def usd_to_btc(usd_amount):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    # Get the current BTC to USD exchange rate
    btc_price_in_usd = data['bitcoin']['usd']

    # Convert USD to BTC
    btc_amount = usd_amount / btc_price_in_usd

    # Format the result with 8 decimal places
    return round(btc_amount, 8)
