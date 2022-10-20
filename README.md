# RSA Cracker

This is a tool to be used for cracking weak RSA implementations.  It additionally can perform basic RSA operations such as encryption and decryption.

Note that there are probably better tools out there for whatever your needs may be.  This tool is designed to be simple and intended to be a learning experience for me as I learn and implement new types of attacks into it.  You are encouraged to look through the code and try to understand how each attack works.


## Setup

```
git clone https://github.com/danieltaylor/rsa-cracker.git
cd rsa-cracker
pip install -r requirements.txt
```


## Usage

`python rsa_cracker.py`

If executed without any args as shown above, the program will prompt for the setting of variables and selection of modes.

Alternatively, arguments may be passed to the program in order to skip the menu or make it easier to repeat actions with similar values.

See `python rsa_cracker.py --help` for more details:

```
usage: rsa_cracker.py [-h] [-m PLAINTEXT] [-c CIPHERTEXT] [-n MODULUS] [-e PUBLICEXP] [-d PRIVATEEXP] [-1] [-2] [-3]

RSA Cracker

options:
  -h, --help            show this help message and exit
  -m PLAINTEXT, --plaintext PLAINTEXT
                        plaintext to be encrypted
  -c CIPHERTEXT, --ciphertext CIPHERTEXT
                        ciphertext to be decrypted
  -n MODULUS, --modulus MODULUS
                        modulus value
  -e PUBLICEXP, --publicexp PUBLICEXP
                        public exponent (default = 65537)
  -d PRIVATEEXP, --privateexp PRIVATEEXP
                        private exponent
  -1, --crack           crack mode
  -2, --encrypt         encrypt mode
  -3, --decrypt         decrypt mode
```


## Recommended Resources

### Reading
- https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- https://www.quaxio.com/exploring_three_weaknesses_in_rsa/

### Other Tools
- https://github.com/RsaCtfTool/RsaCtfTool
- https://www.dcode.fr/rsa-cipher
- http://www.factordb.com
