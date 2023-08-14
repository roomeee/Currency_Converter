import requests

from key import apikey


def get_currency_symbols(api_key):
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    headers = {
        "apikey": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        symbols_data = response.json()
        return symbols_data['symbols']
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


def main():
    api_key = "cV1WchbAWfv4YdWSNVm9YzKKcrNovgK3"

    symbols = get_currency_symbols(api_key)

    if symbols:
        print("Available currency symbols:")
        for symbol in symbols:
            print(symbol)

        from_currency = input("Enter the base currency symbol (e.g., USD): ").upper()
        to_currency = input("Enter the target currency symbol (e.g., EUR): ").upper()
        amount = float(input("Enter the amount to convert: "))

        url = "https://api.apilayer.com/exchangerates_data/convert"
        payload = {
            "to": to_currency,
            "from": from_currency,
            "amount": amount
        }
        headers = {
            "apikey": api_key
        }

        response = requests.get(url, params=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print("API Response:", result)  # Print the full API response for debugging
            converted_amount = result.get('result')

            if converted_amount is not None:
                print(f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")
            else:
                print("Conversion result not found in the API response.")
        else:
            print(f"Request failed with status code: {response.status_code}")

if __name__ == "__main__":
    main()
