# Python Project Crypto Currency Converter
#
# DESCRIPTION
# Build a Crypto-currency converter using Python
# The converter converts the value of popular Cryptocurrencies (BTC, ETH, NEO, LTC etc.)
# in USD, EUR, JPY, GBP, AUD and Taka.
#
# ADDITINAL REQUIREMENTS
# Rank the currencies according to the current market surge rate analyzing data of the last 3 months.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from tkinter import *
import tkinter as tk
from tkinter import ttk

# Real time Currency conversion using coinmarket api
class CurrencyConverter():

    def convert(crypto,fiat,amount):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
          'symbol':crypto,
          'convert':fiat
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': '631bd971-1ee9-4871-906a-843abe55882e',

        }

        session = Session()
        session.headers.update(headers)
        int_amount = amount

        try:
          response = session.get(url, params=parameters)
          data = json.loads(response.text)
          amount = round(data['data'][crypto]['quote'][fiat]['price']*int_amount, 2)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
          print(e)

        return amount


class App(tk.Tk):


    def __init__(self):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'

        self.configure(background = '#2D496D')
        self.geometry("500x200")

        # Title
        self.title = Label(self, text = 'Crypto Currency Convertor',  fg = 'white', bg = '#2D496D', borderwidth = 3)
        self.title.config(font = ('Courier',15,'bold'))

        self.title.place(x = 100 , y = 5)

        # label
        self.crypto_label = Label(self, text = 'Crypto Currency',  fg = 'white', bg = '#2D496D', borderwidth = 3)
        self.crypto_label.config(font = ('Courier',13,'bold'))
        self.fiat_label = Label(self, text = 'Fiat Currency',  fg = 'white', bg = '#2D496D', borderwidth = 3)
        self.fiat_label.config(font = ('Courier',13,'bold'))

        # Retrieve list of currencies fron currency.txt
        with open('currencyList.txt') as f:
            crypto_currency_line = f.readline()
            fiat_currency_line = f.readline()

        stripped_crypto_currency_line = crypto_currency_line.strip()
        crypto_currency_list = stripped_crypto_currency_line.split()

        stripped_fiat_currency_line = fiat_currency_line.strip()
        fiat_currency_list = stripped_fiat_currency_line.split()

        # Dropdown
        self.crypto_currency_variable = StringVar(self)
        self.crypto_currency_variable.set("BTC") # default value
        self.fiat_currency_variable = StringVar(self)
        self.fiat_currency_variable.set("USD") # default value

        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.cryto_currency_dropdown = ttk.Combobox(self,textvariable=self.crypto_currency_variable, values= crypto_currency_list, font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.fiat_currency_dropdown = ttk.Combobox(self,textvariable=self.fiat_currency_variable, values= fiat_currency_list, font = font, state = 'readonly', width = 12, justify = tk.CENTER)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self,bd = 3, relief = tk.RIDGE, justify = tk.CENTER,validate='key', validatecommand=valid)
        self.converted_amount_field = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 17, borderwidth = 3)

        # Placement
        self.crypto_label.place(x = 24, y= 90)
        self.fiat_label.place(x = 337, y= 90)
        self.cryto_currency_dropdown.place(x = 30, y= 120)
        self.fiat_currency_dropdown.place(x = 335, y= 120)
        self.amount_field.place(x = 37, y = 150)
        self.converted_amount_field.place(x = 342, y = 150)

        # Convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", command = self.function)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x = 225, y = 135)

    # Restrcts entry requrements for the amout_field box
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

    def function(self):
        amount = float(self.amount_field.get())
        crypto_curr = self.crypto_currency_variable.get()
        fiat_curr = self.fiat_currency_variable.get()

        if crypto_curr == fiat_curr:
            converted_amount = amount

        else:
            converted_amount = CurrencyConverter.convert(crypto_curr,fiat_curr,amount)
            converted_amount = round(converted_amount, 2)

        self.converted_amount_field.config(text = str(converted_amount))


if __name__ == '__main__':
    #converter = CurrencyConverter()
    App()
    mainloop()
