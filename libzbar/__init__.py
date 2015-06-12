from ._ffi import ffi, lib

def zbar_version():
    ver = ffi.new("unsigned[2]")
    lib.zbar_version((ver + 0), (ver + 1))
    return (ver[0], ver[1])


class CEnum(object):
    def __init__(self, lib, names):
        names = [n.strip().split(None, 1)[:1] for n in names.splitlines()]
        names = [n[0] for n in names if n and n[0]]
        vals = [getattr(lib, n) for n in names]
        self._by_name = dict(zip(names, vals))
        self._by_value = dict(zip(vals, names))

    def __getattr__(self, attr):
        try:
            return self._by_name[attr]
        except KeyError:
            raise AttributeError(attr)

    def __getitem__(self, attr):
        return self._by_name[attr]

    def __iter__(self):
        return iter(self._by_name)

    def from_value(self, value, default=None):
        return self._by_value.get(value, default)


def managed(create, args, free):
    o = create(*args)
    if o == ffi.NULL:
        raise MemoryError("%s could not allocate memory" %(create.__name__, ))
    return ffi.gc(o, free)


def refcounted(o, func):
    func(o, 1)
    return ffi.gc(o, lambda o: func(o, -1))


def check(func, args):
    res = func(*args)
    if res != 0:
        raise ValueError("%s%r failed with %s" %(func.__name__, args, res))
    return res



class Scanner(object):
    def __init__(self):
        self._scanner = managed(lib.zbar_image_scanner_create, (),
                                lib.zbar_image_scanner_destroy)
        check(lib.zbar_image_scanner_set_config, (self._scanner, 0, lib.ZBAR_CFG_ENABLE, 1))

    def scan_image(self, image):
        return image.scan(self)


class Image(object):
    def __init__(self, size, data, data_ref=None):
        self.size = size
        self.data = data
        self.data_ref = data_ref
        self._img = managed(lib.zbar_image_create, (),
                            lib.zbar_image_destroy)
        lib.zbar_image_set_format(self._img, lib.ZBAR_FORMAT_GREY)
        lib.zbar_image_set_size(self._img, size[0], size[1])
        lib.zbar_image_set_data(self._img, self.data, size[0] * size[1], ffi.NULL)

    @classmethod
    def from_im(cls, im):
        if im.mode != "L":
            im = im.convert("L")
        data = ffi.new("uint8_t[]", im.tobytes())
        return cls(im.size, data)

    @classmethod
    def from_np(cls, size, arr):
        if arr.dtype.itemsize != 1:
            arr = arr.astype("uint8")
        return cls(size, ffi.cast("uint8_t*", arr.ctypes.data), data_ref=arr)

    def scan(self, scanner=None):
        scanner = scanner or Scanner()
        n = lib.zbar_scan_image(scanner._scanner, self._img)
        if n < 0:
            raise ValueError("Error while scanning image: %s" %(n, ))
        symbol = lib.zbar_image_first_symbol(self._img)
        symbols = []
        while symbol != ffi.NULL:
            symbols.append(Symbol(symbol))
            symbol = lib.zbar_symbol_next(symbol)
        return symbols


class Symbol(object):
    types = CEnum(lib, """
        ZBAR_NONE        =      0,  /**< no symbol decoded */
        ZBAR_PARTIAL     =      1,  /**< intermediate status */
        ZBAR_EAN8        =      8,  /**< EAN-8 */
        ZBAR_UPCE        =      9,  /**< UPC-E */
        ZBAR_ISBN10      =     10,  /**< ISBN-10 (from EAN-13). @since 0.4 */
        ZBAR_UPCA        =     12,  /**< UPC-A */
        ZBAR_EAN13       =     13,  /**< EAN-13 */
        ZBAR_ISBN13      =     14,  /**< ISBN-13 (from EAN-13). @since 0.4 */
        ZBAR_I25         =     25,  /**< Interleaved 2 of 5. @since 0.4 */
        ZBAR_CODE39      =     39,  /**< Code 39. @since 0.4 */
        ZBAR_PDF417      =     57,  /**< PDF417. @since 0.6 */
        ZBAR_QRCODE      =     64,  /**< QR Code. @since 0.10 */
        ZBAR_CODE128     =    128,  /**< Code 128 */
        ZBAR_SYMBOL      = 0x00ff,  /**< mask for base symbol type */
        ZBAR_ADDON2      = 0x0200,  /**< 2-digit add-on flag */
        ZBAR_ADDON5      = 0x0500,  /**< 5-digit add-on flag */
        ZBAR_ADDON       = 0x0700,  /**< add-on flag mask */
    """)

    def __init__(self, symbol):
        self._sym = refcounted(symbol, lib.zbar_symbol_ref)

    @property
    def type(self):
        return self.types.from_value(lib.zbar_symbol_get_type(self._sym))

    @property
    def data(self):
        data = lib.zbar_symbol_get_data(self._sym)
        return bytes(ffi.buffer(data, lib.zbar_symbol_get_data_length(self._sym)))

    @property
    def quality(self):
        """ An unscaled, relative quantity: larger values are better than
            smaller values, where "large" and "small" are application
            dependent.
            
            Note: expect the exact definition of this quantity to change as the
            metric is refined. Currently, only the ordered relationship
            between two values is defined and will remain stable in the future.
            """
        return lib.zbar_symbol_get_quality(self._sym)

    @property
    def locator(self):
        """ Returns a list of (x, y) points in the locator polygon. """
        result = []
        for pt in range(lib.zbar_symbol_get_loc_size(self._sym)):
            result.append((
                lib.zbar_symbol_get_loc_x(self._sym, pt),
                lib.zbar_symbol_get_loc_y(self._sym, pt),
            ))
        return result

    def __repr__(self):
        return "<Symbol type=%s quality=%s data=%r locator=%r>" %(
            self.type, self.quality, self.data, self.locator,
        )
