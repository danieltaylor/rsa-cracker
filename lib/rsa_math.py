import math


def mod_exp(coef, exp, mod, verbose=False):
	vals = [1, coef % mod]
	for i in range(len(bin(exp)) - 2):
		vals.append((vals[i + 1] ** 2) % mod)
	if verbose:
		print(vals)
	result = 1
	for i in range(len(bin(exp)) - 2):
		mask = 0b1 << i
		if mask & exp != 0:
			if verbose:
				print(result, ' * ', vals[i + 1], ' % ', mod, ' = ', (result * vals[i + 1]) % mod)
			result = (result * vals[i + 1]) % mod
	return result


def mod_inverse(a, n):
	t = 0
	r = n
	new_t = 1
	new_r = a

	while new_r != 0:
		quotient = r // new_r
		(t, new_t) = (new_t, t - quotient * new_t)
		(r, new_r) = (new_r, r - quotient * new_r)

	if r > 1:
		return 'a is not invertible'
	if t < 0:
		t = t + n

	return t


def gcd(a, b):
	if b == 0:
		return max(a, -a)
	else:
		return gcd(b, a % b)


# Source: https://stackoverflow.com/questions/47854635/square-root-of-a-number-greater-than-102000-in-python-3
def isqrt(x):
	"""Return the integer part of the square root of x, even for very
	large integer values.
	"""
	if x < 0:
		raise ValueError('square root not defined for negative numbers')
	if x < (1 << 50):  # 2**50 == 1,125,899,906,842,624
		return int(math.sqrt(x))  # use math's sqrt() for small parameters
	n = int(x)
	if n <= 1:
		return n  # handle sqrt(0)==0, sqrt(1)==1
	# Make a high initial estimate of the result (a little lower is slower!!!)
	r = 1 << ((n.bit_length() + 1) >> 1)
	while True:
		newr = (r + n // r) >> 1  # next estimate by Newton-Raphson
		if newr >= r:
			return r
		r = newr


# Source: https://stackoverflow.com/questions/356090/how-to-compute-the-nth-root-of-a-very-big-integer
def find_invpow(x,n):
	"""Finds the integer component of the n'th root of x,
	an integer such that y ** n <= x < (y + 1) ** n.
	"""
	high = 1
	while high ** n < x:
		high *= 2
	low = high // 2
	while low < high:
		mid = (low + high) // 2
		if low < mid and mid**n < x:
			low = mid
		elif high > mid and mid**n > x:
			high = mid
		else:
			return mid
	return mid + 1
