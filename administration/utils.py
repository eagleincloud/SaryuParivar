import math
import random

def generate_otp_code(size=6):
    digits = "0123456789"
    OTP = ""
    for i in range(size):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP
