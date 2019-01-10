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
plain = "Ciao come va? Io tutto bene e tu?"
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