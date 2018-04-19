import sys
from cffi import FFI
ffi = FFI()

ffi.cdef("""
	int setup(int party, int number);
""")

addition = ffi.dlopen("/home/phil/Schreibtisch/Uni/MA/Forschungsprojekt/word2vec_Impl/Umsetzung/desm-mpc/obliv_c_desm/oblivc_test/libaddition.so")

party = int(sys.argv[1])
num = int(sys.argv[2])

addition.setup(party, num)
