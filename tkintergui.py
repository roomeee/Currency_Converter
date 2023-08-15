import tkinter as tk
from tkinter import ttk
import requests
from key import api_key

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
        "apikey": api_key
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
style.configure("TCombobox", font=("Helvetica", 12))

currency_symbols = get_currency_symbols(api_key)

from_currency_var = tk.StringVar()
to_currency_var = tk.StringVar()
amount_var = tk.DoubleVar()

# Main frame
main_frame = ttk.Frame(app, padding=20)
main_frame.pack(fill="both", expand=True)

# Header
header_label = ttk.Label(main_frame, text="Currency Converter", font=("Helvetica", 24, "bold"))
header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 10))

# From Currency
from_currency_label = ttk.Label(main_frame, text="From Currency:")
from_currency_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

from_currency_combobox = ttk.Combobox(main_frame, values=list(currency_symbols.keys()), textvariable=from_currency_var)
from_currency_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# To Currency
to_currency_label = ttk.Label(main_frame, text="To Currency:")
to_currency_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

to_currency_combobox = ttk.Combobox(main_frame, values=list(currency_symbols.keys()), textvariable=to_currency_var)
to_currency_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Amount
amount_label = ttk.Label(main_frame, text="Amount:")
amount_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

amount_entry = ttk.Entry(main_frame, textvariable=amount_var)
amount_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Convert button
convert_button = ttk.Button(main_frame, text="Convert", command=perform_conversion)
convert_button.grid(row=4, column=0, columnspan=2, pady=20)

# Result label
result_label = ttk.Label(main_frame, text="", font=("Helvetica", 14, "italic"))
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Making the columns and rows expand to fill available space
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

app.mainloop()
