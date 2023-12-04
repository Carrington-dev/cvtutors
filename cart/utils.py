import math, random

SHIPPING_FEE_PER_COUNTRY = 100
def _generate_cart_id():
    cart_id = ""
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890()!*$#%&^@'.lower()
    cart_id_length = 50
    c_length = len(characters)

    digits = "0123456789"
    OTP = ""
    for i in range(30) :
        OTP += characters[math.floor(random.random() * c_length)]
    return OTP