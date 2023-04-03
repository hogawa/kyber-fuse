#include <stdio.h>
#include <string.h>
#include "kyber_fused.h"

int main() {
    uint8_t sk_a[KYBER_SECRETKEYBYTES];
    uint8_t pk_a[KYBER_PUBLICKEYBYTES];
    uint8_t ss_a[KYBER_SSBYTES];
    uint8_t ss_b[KYBER_SSBYTES];
    uint8_t ct_b[KYBER_CIPHERTEXTBYTES];

    printf("KYBER_K = %d\n\n", KYBER_K);

    // Alice generates a public-private Kyber keypair
    crypto_kem_keypair(pk_a, sk_a);

    printf("Alice's private key (%d bytes) = 0x", KYBER_SECRETKEYBYTES);
    for (int i = KYBER_SECRETKEYBYTES - 1; i >= 0; i--) {
        printf("%02x", sk_a[i]);
    }

    printf("\n\n");

    printf("Alice's public key (%d bytes) = 0x", KYBER_PUBLICKEYBYTES);
    for (int i = KYBER_PUBLICKEYBYTES - 1; i >= 0; i--) {
        printf("%02x", pk_a[i]);
    }

    printf("\n\n");

    // Bob derives a shared secret and a ciphertext from Alice's public key
    crypto_kem_enc(ct_b, ss_b, pk_a);

    printf("Bob's shared secret (%d bytes) = 0x", KYBER_SSBYTES);
    for (int i = KYBER_SSBYTES - 1; i >= 0; i--) {
        printf("%02x", ss_b[i]);
    }

    printf("\n\n");

    printf("Bob's ciphertext (%d bytes) = 0x", KYBER_CIPHERTEXTBYTES);
    for (int i = KYBER_CIPHERTEXTBYTES - 1; i >= 0; i--) {
        printf("%02x", ct_b[i]);
    }

    printf("\n\n");

    // Alice derives a shared secret from Bob's ciphertext
    crypto_kem_dec(ss_a, ct_b, sk_a);

    printf("Alice's shared secret (%d bytes) = 0x", KYBER_SSBYTES);
    for (int i = KYBER_SSBYTES - 1; i >= 0; i--) {
        printf("%02x", ss_a[i]);
    }

    printf("\n\n");

    // Check if shared secrets match
    if (memcmp(ss_a, ss_b, KYBER_SSBYTES) == 0) {
        printf("[PASS] Alice and Bob's shared secrets match\n\n");
    }
    else {
        printf("[FAIL] Alice and Bob's shared secrets don't match!\n\n");
    }

    return 0;
}
