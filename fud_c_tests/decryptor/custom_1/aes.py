from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES


# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        #self.key = md5(key.encode('utf8')).hexdigest()
        self.key = key.encode('utf8')

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        #return b64encode(cipher.encrypt(raw))
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        enc = enc
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8')


##
# MAIN
# Just a test.
msg = "AAAAAAAAAAAAAAAA"
pwd = "YELLOW SUBMARINE"

print('Ciphertext:', AESCipher(pwd).encrypt(msg))