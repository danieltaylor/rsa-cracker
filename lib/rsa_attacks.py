from lib.rsa_math import *
from lib.print_colors import *

from sympy import nextprime, prevprime, factorint
import requests


AUTO_FACTOR_BIT_LENGTH = 110


def small_e(c, e):
	if e <= 7:
		m = find_invpow(c, e)
		return m
	else:
		return None


def check_duplicate_primes(n, sqrt_n):
	if sqrt_n**2 == n:
		p = sqrt_n
		q = sqrt_n
		return p, q
	else:
		return None


def check_consecutive_primes(n, sqrt_n):
	prev_prime = prevprime(sqrt_n)
	next_prime = nextprime(sqrt_n)
	if sqrt_n * next_prime == n:
		p = sqrt_n
		q = next_prime
		return p, q
	elif prev_prime * next_prime == n:
		p = prev_prime
		q = next_prime
		return p, q
	else:
		return None


def check_easily_factorable(n):
	if n.bit_length() < AUTO_FACTOR_BIT_LENGTH:
		# TODO handle when n has more than 2 factors
		factors = sorted(list(factorint(n)))
		p = factors[0]
		q = factors[1]
		return p, q
	else:
		return None


def check_factordb(n):
	factordb_json = requests.get(f'http://factordb.com/api?query={n}').json()
	if factordb_json['status'] == 'FF':
		p = int(factordb_json['factors'][0][0])
		q = int(factordb_json['factors'][1][0])
		return p, q
	else:
		return None


def brute_force_factorization(n):
	print()
	print('Attempt to factor n into p and q anyways?  (Not recommended for large values of n, may be computationally infeasible.)')
	print('n is a', n.bit_length(), 'bit integer.  ')
	if 'n' not in input('  y/n: '):
		print('Factoring...')
		factors = factorint(n)
		num_factors = 0
		for f in factors:
			num_factors += factors[f]
		if num_factors == 2:
			print('Successfully factored n!')
			factors = sorted(list(factors))
			p = factors[0]
			q = factors[1]
			return p, q
		else:
			print(COLORS.RED + 'Unable to factor n into two primes, please verify value of n.' + COLORS.RESET)
			print('The factors of n are:')
			print(factors)
		return None
