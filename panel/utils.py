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
    # d = datetime.date(yr,mt,dt)
    # current_date = d.strftime("%Y%m%d")
    # order_num = str(current_date) + str(id)
    fin =  _generate_order_id()
    order_num = fin[0] + str(yr) + fin[1] + str(mt) + fin[2] + str(dt) + fin[3]
    return order_num + str(id)