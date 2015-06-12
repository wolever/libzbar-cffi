libqrencode: fast QR code encoding for Python
=============================================

Fast, robust, and slightly less incomplete cffi-based Python bindings for
libqrencode (http://fukuchi.org/works/qrencode/index.en.html).

Python 2, Python 3, and PyPy compatible!

Installing
----------

::

    $ pip install libqrencode-cffi


Examples
--------

::

    >>> import libqrencode as qr
    >>> qrc = qr.QRCode("Hello, world!")

    # The raw QR code can be accessed, where each item is a bitfield containing
    # information about that portion of the code (see DATA_* constants).
    >>> qrc.get_raw_data()
    [193, 193, 193, 193, ...  3, 2, 2, 3, 3]

    # If PIL is installed, a PIL image of the QR code can be created:
    >>> qrc.get_im(border=3)
    <PIL.Image.Image image mode=L size=81x81 at ...>

    # And if lxml.etree / xml.etree is available, an SVG can be generated:
    >>> qrc.get_svg_etree()
    <Element g at ...>
    >>> qrc.get_svg_string()
    '<g><rect fill="white" height="21" width="21" x="0" y="0"/>...<rect fill="black" height="1" width="1" x="20" y="19"/></g>'


Constants
---------

Encoding modes (see https://en.wikipedia.org/wiki/QR_code#Encoding):

* ``MODE_NUL`` (internal to qrencode)
* ``MODE_NUM``
* ``MODE_AN``
* ``MODE_8`` (default)
* ``MODE_KANJI``
* ``MODE_STRUCTURE`` (not fully supported by libqrencode)
* ``MODE_ECI`` (not fully supported by libqrencode)
* ``MODE_FNC1FIRST`` (not fully supported by libqrencode)
* ``MODE_FNC1SECOND`` (not fully supported by libqrencode)


Error correction modes:

* ``ECLEVEL_L`` (7%; default)
* ``ECLEVEL_M`` (15%)
* ``ECLEVEL_Q`` (25%)
* ``ECLEVEL_H`` (30%)


Raw data bitmasks:

* ``DATA_BW`` (1=black/0=white)
* ``DATA_DATA_AND_ECC`` (data and ecc code area)
* ``DATA_FORMAT_INFO`` (format information)
* ``DATA_VERSION_INFO`` (version information)
* ``DATA_TIMING_PATTERN`` (timing pattern)
* ``DATA_ALIGNMENT_PATTERN`` (alignment pattern)
* ``DATA_FINDER_PATTERN`` (finder pattern and separator)
* ``DATA_NON_DATA`` (non-data modules (format, timing, etc.))
