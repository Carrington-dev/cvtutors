def convert_now(from_currency, to_currency, amount):
    # try:
    #     from forex_python.converter import CurrencyRates

    #     cr = CurrencyRates()

        # amount = int(input("Please enter the amount you want to convert: "))

        # from_currency = input("Please enter the currency code that has to be converted: ").upper()

        # to_currency = input("Please enter the currency code to convert: ").upper()

        # print("You are converting", amount, from_currency, "to", to_currency,".")

        # output = cr.convert(from_currency, to_currency, amount)

    # except:
    output = float(amount)/15.5

    # print("The converted rate is:", output)
    return output

import datetime
import random
import math

def _generate_order_id():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.upper()
    c_length = len(characters)

    OTP = ""
    for i in range(4) :
        OTP += characters[math.floor(random.random() * c_length)]
    return OTP

def order_generate_number(id):
    
    yr = int(datetime.date.today().strftime("%Y"))
    dt = int(datetime.date.today().strftime("%d"))
    mt = int(datetime.date.today().strftime("%m"))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")
    order_num = str(current_date) + str(id)
    return _generate_order_id() + "-" + order_num