libzbar: efficient cffi-based bindings for zbar
===============================================

Python cffi-based bindings for zbar (http://zbar.sourceforge.net/) designed to
be as efficient as possible.

Python 2, Python 3, and PyPy compatible!

Note: currently a work in progress. Entirely functional and production-ready
(see `NumPy note`_), but missing some configuration options.


Installation
------------

::

    $ pip install libzbar-cffi


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


NumPy Note
----------

When using the ``Image.from_np(…)`` constructor a pointer to the underlying
array is passed directly to ``zbar``. The array's size and dtype are sanity
checked, but at the moment the `ctypes flags`__ are ignored, so Strange Things
might happen if the underyling array isn't a straight forward
`uint8_t[size[0] * size[1]]`.

Additionally, the array *should not be changed* for the lifecycle of the
``Image``, as this could invalidate the data pointer.


__ http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.ctypes.html#numpy.ndarray.ctypes
