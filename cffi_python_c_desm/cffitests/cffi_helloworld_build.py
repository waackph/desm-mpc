from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_cffi_hello",
r""" 	#include<stdio.h>
	int hello(char* str){
		printf("%s", str);
		return 1;
	}
""")

ffibuilder.cdef("int hello(char*);")

if __name__ == "__main__":
	ffibuilder.compile(verbose=True)
