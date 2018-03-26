from _cffi_hello import ffi, lib

hello = ffi.new("char[]", b"Hello World\n")

print(hello)

lib.hello(hello)
