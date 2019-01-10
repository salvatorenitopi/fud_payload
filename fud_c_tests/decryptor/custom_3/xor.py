def Crypt(aString, key):
    kIdx = 0
    cryptStr = ""   # empty 'crypted string to be returned

    # loop through the string and XOR each byte with the keyword
    # to get the 'crypted byte. Add the 'crypted byte to the
    # 'crypted string
    for x in range(len(aString)):
        cryptStr = cryptStr + chr( ord(aString[x]) ^ ord(key[kIdx]))
        # use the mod operator - % - to cyclically loop through
        # the keyword
        kIdx = (kIdx + 1) % len(key)

    return cryptStr




def strToHex(aString):
    hexStr = ""
    for x in aString:
        hexStr = hexStr + "%02X " % ord(x)

    return hexStr

# self test routine

print "\nTesting PEcrypt!"
print "----------------\n"

keyStr = "This is a key"
testStr = "The quick brown fox jumps over the lazy dog!"


print Crypt (testStr, keyStr)
print Crypt (Crypt (testStr, keyStr), keyStr)

print strToHex (Crypt (testStr, keyStr))
print strToHex (Crypt (Crypt (testStr, keyStr), keyStr))