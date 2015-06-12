import os

from cffi import FFI

ffi = FFI()

ffi.set_source("libzbar._ffi",
    """
        #include <zbar.h>
        #define fourcc(a, b, c, d)                      \
            ((uint32_t)(a) | ((uint32_t)(b) << 8) |     \
             ((uint32_t)(c) << 16) | ((uint32_t)(d) << 24))
        unsigned long ZBAR_FORMAT_GREY = fourcc('Y', '8', '0', '0');
    """,
    libraries=["zbar"],
)
with open(os.path.join(os.path.dirname(__file__), "zbar-0.10-noifdefs.h")) as f:
    ffi.cdef(
        f.read() + "\n" +
        "extern unsigned long ZBAR_FORMAT_GREY;\n"
    )

if __name__ == "__main__":
    ffi.compile()
