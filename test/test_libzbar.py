import os

from PIL import Image
import pytest

import libzbar as zbar

path = lambda *a: os.path.join(os.path.dirname(__file__), *a)

def test_version():
    assert zbar.zbar_version() == (0, 10)

@pytest.mark.parametrize("img,expected", [
    ("qr-null-byte.png", b"123\x00abc"),
    ("qr-numeric.png", b"12345"),
])
def test_scan_simple(img, expected):
    im = Image.open(path(img))
    symbols = zbar.Image.from_im(im).scan()
    assert len(symbols) == 1
    symbol = symbols[0]
    assert symbol.data == expected
