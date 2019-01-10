import random

def randomize (plain, junk):
	charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
	out = []
	for i in plain:
		for j in range(junk):
			out.append (random.choice(charset))
		out.append (i)

	return "".join(out)

def derandomize (cipher, junk):
	out = []
	counter = 0
	for i in range(0, len(cipher)):
		counter += 1
		if ((counter % (junk + 1)) == 0):
			out.append (cipher[i])

	return "".join(out)

def cvar (text, size):
	out = "char buff[] = "
	w = [text[i:i+size] for i in range(0, len(text), size)]

	for i in range(0, len(w)):
		out += "\n\"" + w[i] + "\""

	out += ";"

	return out

####################################################################################

junk = 4
plain = "PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA"
out = []

a = randomize (plain, junk)
b = derandomize (a, junk)

print "ENCODED:"
print a
print 
print "DECODED:"
print b
print 
print "ENCODED SIZE: " + str(len(a))
print "DECODED SIZE: " + str(len(b))

print cvar (a, 64)

print ":".join("{:02x}".format(ord(c)) for c in a)