import random

import barcode

EAN = barcode.get_barcode_class('ean8')

from barcode.writer import ImageWriter

def make_barcode(text):
    try:
        ean = EAN(str(text), writer=ImageWriter())
    except:
        return "eRROR"
    return ean
def predict(f):
    # результат работы нейросети
    return random.random()