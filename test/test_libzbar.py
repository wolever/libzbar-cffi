import os

import pytest
import numpy as np
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


@pytest.mark.parametrize("img,expected", test_images)
def test_from_np(img, expected):
    im = Image.open(path(img))
    arr = np.array(im)
    symbols = zbar.Image.from_np(im.size, arr).scan()
    assert len(symbols) == 1
    symbol = symbols[0]
    assert symbol.data == expected
