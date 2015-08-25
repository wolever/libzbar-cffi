import os

import pytest
try:
    import numpy as np
except ImportError:
    np = None
from PIL import Image

import libzbar as zbar

path = lambda *a: os.path.join(os.path.dirname(__file__), *a)

def test_version():
    assert zbar.zbar_version() == (0, 10)

test_images = [
    ("qr-null-byte.png", b"123\x00abc"),
    ("qr-numeric.png", b"12345"),
]

@pytest.mark.parametrize("img,expected", test_images)
def test_scan_simple(img, expected):
    im = Image.open(path(img))
    symbols = zbar.Image.from_im(im).scan()
    assert len(symbols) == 1
    symbol = symbols[0]
    assert symbol.data == expected

ean13_im = Image.open(path("ean13-example.png"))

def test_scan_no_qr_code():
    symbols = zbar.Image.from_im(ean13_im).scan()
    assert symbols == []

def test_scan_ean13():
    ean13_type = zbar.symbol_types.ZBAR_EAN13
    symbols = zbar.Image.from_im(ean13_im).scan(symbol_type=ean13_type)
    assert len(symbols) == 1
    assert symbols[0].type == "ZBAR_EAN13"

def test_scan_all_symbol_types():
    symbols = zbar.Image.from_im(ean13_im).scan(symbol_type=0)
    assert len(symbols) == 1

@pytest.mark.parametrize("img,expected", test_images)
@pytest.mark.skipif(np is None, reason="requires numpy")
def test_from_np(img, expected):
    im = Image.open(path(img))
    arr = np.array(im)
    symbols = zbar.Image.from_np(im.size, arr).scan()
    assert len(symbols) == 1
    symbol = symbols[0]
    assert symbol.data == expected

@pytest.mark.skipif(np is None, reason="requires numpy")
def test_np_invalid_size():
    arr = np.zeros(1)
    with pytest.raises(ValueError):
        zbar.Image.from_np((1000, 1000), arr)
