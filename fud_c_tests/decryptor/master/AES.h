// https://gist.github.com/giuscri/4bfbdc160dd0741341fa5c596f92e227


#include <openssl/conf.h>
#include <openssl/evp.h>

#include <assert.h>
#include <string.h>
#include <stdio.h>

#define MAX_PLAINTEXT_BYTES 160
#define WRAPLINE_AT 32

int
encrypt_aes_ecb(unsigned char * plaintext, int plaintext_length,
                unsigned char * key, unsigned char * ciphertext)
{
    int ciphertext_length = 0;
    int length = 0;

    EVP_CIPHER_CTX * ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        perror("EVP_CIPHER_CTX_new()");
        exit(-1);
    }

    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)) {
        perror("EVP_EncryptInit_ex()");
        exit(-1);
    }

    if (1 != EVP_EncryptUpdate(ctx, ciphertext, &length, plaintext, plaintext_length)) {
        perror("EVP_EncryptUpdate()");
        exit(-1);
    }
    ciphertext_length += length;

    if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + length, &length)) {
        perror("EVP_EncryptFinal_ex()");
        exit(-1);
    }
    ciphertext_length += length;

    EVP_CIPHER_CTX_free(ctx);

    return ciphertext_length;
}

int
decrypt_aes_ecb(unsigned char * ciphertext, int ciphertext_length,
                unsigned char * key, unsigned char * plaintext)
{
    int plaintext_length = 0;
    int length = 0;

    EVP_CIPHER_CTX * ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        perror("EVP_CIPHER_CTX_new()");
        exit(-1);
    }

    if (1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)) {
        perror("EVP_DecryptInit_ex()");
        exit(-1);
    }

    if (1 != EVP_DecryptUpdate(ctx, plaintext, &length, ciphertext, ciphertext_length)) {
        perror("EVP_DecryptUpdate()");
        exit(-1);
    }
    plaintext_length += length;

    if (1 != EVP_DecryptFinal_ex(ctx, plaintext + length, &length)) {
        perror("EVP_DecryptFinal_ex()");
        exit(-1);
    }
    plaintext_length += length;

    EVP_CIPHER_CTX_free(ctx);

    return plaintext_length;
}

int
main(int argc, char ** argv)
{
    unsigned char * key = NULL;

    if (argc > 1) {
        key = (unsigned char *)strndup(argv[1], 16);
    } else {
        key = (unsigned char *)"YELLOW SUBMARINE";
    }

    assert(strlen((const char *)key) == 16);

    unsigned char * plaintext = NULL;

    #ifdef DEBUG
        plaintext = "AAAAAAAAAAAAAAAA";
        assert(strlen(plaintext) == 16);
    #else
        // Counting bytes here is a little tricky.
        // Indeed, fgets() reads at most less (!)
        // than `size` bytes. Also, a final \x00
        // is appended after the last character of
        // the buffer. Since we need to read MAX_PLAINTEXT_BYTES,
        // we need to set `size` to MAX_... + 1 (such to read them all)
        // and allocate memory for MAX_... + 1 bytes, since fgets() will
        // always try to write past the number of bytes read.
        plaintext = calloc(MAX_PLAINTEXT_BYTES + 1, 1);
        fgets((char *)plaintext, MAX_PLAINTEXT_BYTES + 1, stdin);
    #endif

    int plaintext_length = strlen((const char *)plaintext);
    unsigned char * ciphertext = calloc((plaintext_length + 16 - plaintext_length % 16) * 2, 1);
    int ciphertext_length = encrypt_aes_ecb(plaintext, plaintext_length, key, ciphertext);

    #ifdef DEBUG
        unsigned char * expected = "\xe4\x40\x85\xfa\x2b\xda\x33\xd8\x6a\xa3\x40"
                                   "\xb4\xc1\x6c\x05\xad\x60\xfa\x36\x70\x7e\x45"
                                   "\xf4\x99\xdb\xa0\xf2\x5b\x92\x23\x01\xa5";
        assert(strlen(expected) == ciphertext_length);

        for (int i = 0; i < ciphertext_length; ++i) {
            assert(expected[i] == ciphertext[i]);
        }
    #endif

    printf("=> Ciphertext: \n");
    for (int i = 0; i < ciphertext_length; ++i) {
        if (i != 0 && i * 2 % WRAPLINE_AT == 0) printf("\n");
        printf("%02x", ciphertext[i]);
    }
    printf("\n");

    #ifdef DEBUG
        unsigned char * decrypted = calloc(ciphertext_length, 1);
        int decrypted_length = decrypt_aes_ecb(ciphertext, ciphertext_length, key, decrypted);
        assert(decrypted_length == plaintext_length);

        printf("<= Plaintext: \n");
        for (int i = 0; i < decrypted_length; ++i) {
            if (i != 0 && i % WRAPLINE_AT == 0) printf("\n");
            printf("%c", decrypted[i]);
        }
        printf("\n");
        free(decrypted);
    #endif

    #ifndef DEBUG
        free(plaintext);
    #endif

    free(ciphertext);

    return 0;
}