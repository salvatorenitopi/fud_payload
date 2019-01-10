#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *xor_encrypt(const char * message, const char * key) {
    size_t messagelen = strlen(message);
    size_t keylen     = strlen(key);
    char * encrypted  = malloc((messagelen + 1)* sizeof(char));

    int i;
    for(i = 0; i < messagelen; i++) {
        encrypted[i] = message[i] ^ key[i % keylen];
        while (encrypted[i] >90) encrypted[i]-=10;
        while (encrypted[i] <65) encrypted[i]+=10;
    }
    encrypted[messagelen] = '\0';
    return encrypted;
}

int main () {
	const char key [] = "CHIAVE";
	const char SHELLCODE[] = "LOL CIAO";

	printf ("%s", xor_encrypt(xor_encrypt(SHELLCODE, key), key));

	exit (0);
}