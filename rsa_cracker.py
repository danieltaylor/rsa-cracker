# from lib.rsa_math import *
from lib.rsa_ops import *
from lib.rsa_attacks import *
from lib.print_colors import *

from sympy.ntheory import factorint
import argparse
import os

# TODO:
# deal with invalid n values for easily factorable and factordb checks
# add ability to submit multiple ciphertexts for Chinese Remainder Theorem attack?
# code cleanup

ALL_VALUES = ['m', 'c', 'n', 'e', 'd']
ALL_VALUES_LONG = ['plaintext', 'ciphertext', 'modulus', 'public exponent', 'private exponent']
OPTIONS = ['Crack', 'Encrypt', 'Decrypt', 'Set Variables', 'Generate Keypair', 'Help', 'Quit']


def main():
	known_values = dict()
	known_values['e'] = 65537

	parser = argparse.ArgumentParser(description='RSA Cracker')
	parser.add_argument('-m', '--plaintext', required=False, help='plaintext to be encrypted')
	parser.add_argument('-c', '--ciphertext', required=False, help='ciphertext to be decrypted')
	parser.add_argument('-n', '--modulus', required=False, help='modulus value')
	parser.add_argument('-e', '--publicexp', required=False, help='public exponent (default = 65537)')
	parser.add_argument('-d', '--privateexp', help='private exponent')
	parser.add_argument('-1', '--crack', help='crack mode', action='store_true')
	parser.add_argument('-2', '--encrypt', help='encrypt mode', action='store_true')
	parser.add_argument('-3', '--decrypt', help='decrypt mode', action='store_true')

	args = parser.parse_args()

	if args.plaintext is not None:
		known_values['m'] = int(args.plaintext)
	if args.ciphertext is not None:
		known_values['c'] = int(args.ciphertext)
	if args.modulus is not None:
		known_values['n'] = int(args.modulus)
	if args.publicexp is not None:
		known_values['e'] = int(args.publicexp)
	if args.privateexp is not None:
		known_values['d'] = int(args.privateexp)

	if args.crack is True:
		option_crack(known_values)
		os.system('clear')
		return
	if args.encrypt is True:
		option_encrypt(known_values)
		os.system('clear')
		return
	if args.decrypt is True:
		option_decrypt(known_values)
		os.system('clear')
		return

	if len(known_values) == 1:
		while option_variables(known_values):
			pass

	while True:
		option = options_menu(known_values)

		if option == '1':
			option_crack(known_values)
		if option == '2':
			option_encrypt(known_values)
		if option == '3':
			option_decrypt(known_values)
		if option == '4':
			while option_variables(known_values):
				pass
		if option == '5':
			option_gen_keypair(known_values)
		if option == '6':
			option_help()
		if option == '7':
			break


# -----MENU AND OPTIONS------

def options_menu(known_values):
	os.system('clear')
	print_header()
	print('Main Menu')
	print()
	print_vars(known_values)
	print_options()

	choice = input('Option selection: ')

	while choice not in map(str, range(1, len(OPTIONS) + 1)):
		choice = input()

	return choice


def option_encrypt(known_values):
	os.system('clear')
	print_header()

	print('Encrypt')
	print()
	print_vars(known_values, ['m', 'e', 'n'])

	if 'n' not in known_values:
		print(COLORS.RED + 'Modulus (n) must be set in order to encrypt!' + COLORS.RESET)
		print()
		input('Press enter to continue.')
		return
	if 'm' not in known_values:
		known_values['m'] = int(input('Enter the message to encrypt: '))

	c = encrypt(known_values['m'], known_values['e'], known_values['n'])

	print('Encrypted value:')
	print(COLORS.GREEN + str(c) + COLORS.RESET)
	print()
	input('Press enter to continue.')


def option_decrypt(known_values):
	os.system('clear')
	print_header()

	print('Decrypt')
	print()
	print_vars(known_values, ['c', 'd', 'n'])

	if 'd' not in known_values:
		print(COLORS.RED + 'Private exponent (d) must be set in order to decrypt!' + COLORS.RESET)
		print()
		input('Press enter to continue.')
		return
	if 'n' not in known_values:
		print(COLORS.RED + 'Modulus (n) must be set in order to decrypt!' + COLORS.RESET)
		print()
		input('Press enter to continue.')
		return
	if 'c' not in known_values:
		known_values['c'] = int(input('Enter the message to decrypt: '))

	m = decrypt(known_values['c'], known_values['d'], known_values['n'])

	print()
	print('Decrypted value:')
	print(COLORS.CYAN + str(m) + COLORS.RESET)
	print()
	print_decoded(m)
	print()
	input('Press enter to continue.')


def option_crack(known_values):
	os.system('clear')
	print_header()

	print('Crack')
	print()
	print_vars(known_values)

	result = crack(known_values)
	if result is None:
		print(COLORS.RED + 'Not enough information provided. Set additional variables if possible.' + COLORS.RESET)
	else:
		p, q = result

		if 'c' in known_values:
			c = known_values['c']
			e = known_values['e']
			n, d = gen_keypair(p, q, e)
			m = decrypt(c, d, n)
			print()
			print('m =', m)
			print()
			print('Attempting to decode m:')
			decode(m)

	print()
	input('Press enter to continue.')


def option_variables(known_values):
	os.system('clear')
	print_header()

	print('Set Variables')
	print()
	print_vars(known_values)

	choice = input('Variable to set (or enter to finish): ')

	if choice == '':
		return False

	while choice not in ALL_VALUES:
		choice = input()
	known_values[choice] = int(input(choice + ' = '))

	return True


def option_gen_keypair(known_values):
	os.system('clear')
	print_header()

	print('Generate Keypair')
	print()

	print(f"Generating n and d using public exponent (e) {known_values['e']}.")
	print()
	print(COLORS.YELLOW + 'n and d will be overwritten.' + COLORS.RESET)
	print()
	p = int(input('p = '))
	q = int(input('q = '))

	known_values['n'], known_values['d'] = gen_keypair(p, q, known_values['e'], True)

	print_vars(known_values, ['n', 'd'])
	input('Press enter to continue.')


def option_help():
	os.system('clear')
	print_header()
	for i in range(len(ALL_VALUES)):
		var = ALL_VALUES[i]
		desc = ALL_VALUES_LONG[i]
		print(COLORS.YELLOW + var + COLORS.RESET + ' = ' + desc)
	print()
	input('Press enter to continue.')



def crack(known_values):
	if 'c' in known_values and 'e' in known_values:
		c = known_values['c']
		e = known_values['e']

		m = small_e(c, e)
		if m:
			print_test_result(True, 'Small e')
			print()
			print(f'  Possible m: {COLORS.CYAN}{m}{COLORS.RESET}')
			print_decoded(m)
			print()
			input('  Press enter to continue.')
			print()
		else:
			print_test_result(False, 'Small e')

	if 'n' in known_values:
		n = known_values['n']

		sqrt_n = isqrt(n)

		functions = [check_duplicate_primes, check_consecutive_primes, check_easily_factorable, check_factordb]
		function_names = ['Duplicate Primes', 'Consecutive Primes', 'Easily Factorable', 'FactorDB Lookup']
		inputs = ['n, sqrt_n', 'n, sqrt_n', 'n', 'n']

		for i in range(len(functions)):
			result = None
			if inputs[i] == 'n, sqrt_n':
				result = functions[i](n, sqrt_n)
			elif inputs[i] == 'n':
				result = functions[i](n)

			if result:
				print_test_result(True, function_names[i])
				print_p_q(result[0], result[1])
				return result
			else:
				print_test_result(False, function_names[i])

		result = brute_force_factorization(n)
		if result:
			return result


# -----DISPLAY HELPERS------

def print_header():
	print(COLORS.RED + '''
                             /)
 __  _   _     _  __  _   _ (/_   _  __
/ (_/_)_(_(_  (__/ (_(_(_(__/(___(/_/ (_
''' + COLORS.RESET)


def print_vars(known_values, values_to_print=ALL_VALUES):
	for var in values_to_print:
		val = known_values[var] if var in known_values else '-'
		print(COLORS.YELLOW + var + COLORS.RESET + ' = ' + str(val))
	print()


def print_options():
	for i in range(1, len(OPTIONS) + 1):
		print(COLORS.MAGENTA +str(i) + COLORS.RESET + ': ' + OPTIONS[i - 1])
	print()


def print_decoded(m):
	decoded = decode(m)

	for encoding, value in decoded.items():
		if value == 'invalid':
			print(f'  {encoding}: invalid')
		else:
			print(f'  {encoding}: {COLORS.GREEN}{value}{COLORS.RESET}')


def print_test_result(success, test_name):
	if success:
		print(COLORS.GREEN + '✓' + COLORS.RESET + ' ' + test_name)
	else:
		print(COLORS.RED + 'X' + COLORS.RESET + ' ' + test_name)


def print_p_q(p, q):
	print(COLORS.GREEN, end='')
	print('  p =', p)
	print('  q =', q)
	print(COLORS.RESET, end ='')


if __name__ == '__main__':
	main()
