import tkinter as tk
from tkinter import ttk
import requests
from key import apikey

def get_currency_symbols(api_key):
    url = api_key
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

def perform_conversion():
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    amount = float(amount_var.get())

    url = "https://api.apilayer.com/exchangerates_data/convert"
    payload = {
        "to": to_currency,
        "from": from_currency,
        "amount": amount
    }
    headers = {
        "apikey": apikey
    }

    response = requests.get(url, params=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        converted_amount = result.get('result')

        if converted_amount is not None:
            result_label.config(text=f"{amount:.2f} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
        else:
            result_label.config(text="Conversion result not found in the API response.")
    else:
        result_label.config(text=f"Request failed with status code: {response.status_code}")

app = tk.Tk()
app.title("Currency Converter")

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

currency_symbols = get_currency_symbols(apikey)

from_currency_var = tk.StringVar()
to_currency_var = tk.StringVar()
amount_var = tk.DoubleVar()

from_currency_label = ttk.Label(app, text="From Currency:")
from_currency_label.pack(pady=5, padx=10, anchor="w")

from_currency_combobox = ttk.Combobox(app, values=list(currency_symbols.keys()), textvariable=from_currency_var)
from_currency_combobox.pack(pady=5, padx=10, fill="x")

to_currency_label = ttk.Label(app, text="To Currency:")
to_currency_label.pack(pady=5, padx=10, anchor="w")

to_currency_combobox = ttk.Combobox(app, values=list(currency_symbols.keys()), textvariable=to_currency_var)
to_currency_combobox.pack(pady=5, padx=10, fill="x")

amount_label = ttk.Label(app, text="Amount:")
amount_label.pack(pady=5, padx=10, anchor="w")

amount_entry = ttk.Entry(app, textvariable=amount_var)
amount_entry.pack(pady=5, padx=10, fill="x")

convert_button = ttk.Button(app, text="Convert", command=perform_conversion)
convert_button.pack(pady=10)

result_label = ttk.Label(app, text="")
result_label.pack(pady=5, padx=10)

app.mainloop()
