libzbar: efficient cffi-based bindings for zbar
===============================================

Python cffi-based bindings for zbar (http://zbar.sourceforge.net/) designed to
be as efficient as possible.

Python 2, Python 3, and PyPy compatible!

Note: currently a work in progress. Entirely functional and production-ready,
but missing some configuration options.


Examples
--------

::

    >>> import libzbar as zb

    # Images can be loaded from PIL images:
    >>> from PIL import Image
    >>> im = Image.open("test/qr-numeric.png")
    >>> zb.Image.from_im(im).scan()
    [<Symbol type=ZBAR_QRCODE quality=1 data='12345' locator=[(12, 12), (12, 75), (75, 75), (75, 12)]>]

    # And from NumPy arrays. Note: if the array has an 8-bit data type (ex,
    # uint8) a pointer to its data will be passed directly into zbar making
    # this method very efficient.
    >>> import numpy as np
    >>> zb.Image.from_np(im.size, np.array(im)).scan()
    [<Symbol type=ZBAR_QRCODE quality=1 data='12345' locator=[(12, 12), (12, 75), (75, 75), (75, 12)]>]
