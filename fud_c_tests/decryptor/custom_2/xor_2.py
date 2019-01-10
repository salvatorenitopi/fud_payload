from itertools import izip, cycle

def xor_crypt_string(data, key='awesomepassword'):
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    return xored
 
 
secret_data = "ABBACCINAT"
secret_key = "CIAO COME VA?"

print xor_crypt_string(secret_data, secret_key)
print xor_crypt_string(xor_crypt_string(secret_data, secret_key), secret_key)