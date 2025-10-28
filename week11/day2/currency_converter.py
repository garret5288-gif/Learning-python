import requests

base_url = "https://api.frankfurter.dev/v1/latest"
try: # Initial test request to check API availability
    response = requests.get(base_url)
except requests.RequestException as e: # Network error handling
    raise SystemExit(f"Network error: {e}")

def convert_currency(currency1, currency2, amount): # Convert currency using Frankfurter API
    try:
        response = requests.get(
            base_url,
            params={"from": currency1, "to": currency2, "amount": amount},
            timeout=10,
        )
    except requests.RequestException as e:
        raise SystemExit(f"Network error: {e}")

    if response.status_code != 200: # Handle non-200 status codes
        try:
            err = response.json()
            msg = err.get("error") or err
        except Exception: # Handle JSON decoding errors
            msg = response.text
        raise SystemExit(f"API error ({response.status_code}): {msg}") # Exit on API error

    try: # Safe JSON parsing
        data = response.json()
    except ValueError:# Handle JSON decoding errors
        raise SystemExit("Invalid JSON response from API.")

    rates = data.get("rates", {})
    if currency2 not in rates: # Validate response shape
        raise SystemExit(f"Unexpected response shape: missing rate for {currency2}.")

    converted_amount = rates[currency2]
    print(f"{amount} {currency1} = {converted_amount} {currency2}")

currency1 = input("Enter the base currency (e.g., USD): ").upper().strip()
currency2 = input("Enter the target currency (e.g., EUR): ").upper().strip()
amount = input("Enter the amount to convert: ").strip()

convert_currency(currency1, currency2, amount)