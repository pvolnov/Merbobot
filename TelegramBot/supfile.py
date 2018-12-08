import barcode

EAN = barcode.get_barcode_class('ean8')

from barcode.writer import ImageWriter

def make_barcode(text):
    ean = EAN('90123412', writer=ImageWriter())
    return ean