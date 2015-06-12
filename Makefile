libzbar/_ffi.so: libzbar/ffi_build.py libzbar/zbar-0.10-noifdefs.h
	python $<

clean:
	rm libzbar/_ffi.*
