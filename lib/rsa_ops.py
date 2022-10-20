from lib.rsa_math import *

from collections import OrderedDict


def gen_keypair(p, q, e, coprime_check=False):
	# check that n is coprime to e (only works if e is prime, e.g. 65537)
	if coprime_check:
		assert (p - 1) % e != 0
		assert (q - 1) % e != 0

	n = p * q
	phi_n = (p - 1) * (q - 1)
	d = mod_inverse(e, phi_n)

	return n, d


def encrypt(m, e, n):
	return mod_exp(m, e, n)


def decrypt(c, d, n):
	return mod_exp(c, d, n)


def decode(m):
	decoded = OrderedDict()

	try:
		decoded['UTF-8 Big-Endian'] = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big').decode()
	except UnicodeDecodeError:
		decoded['UTF-8 Big-Endian'] = 'invalid'

	try:
		decoded['UTF-8 Little-Endian'] = m.to_bytes((m.bit_length() + 7) // 8, byteorder='little').decode()
	except UnicodeDecodeError:
		decoded['UTF-8 Little-Endian'] = 'invalid'

	return decoded
