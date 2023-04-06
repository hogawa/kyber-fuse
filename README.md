# kyber-fuse

Glue code for combining CRYSTALS-Kyber implementation files.

### Motivation

Despite modularity is a key coding practice, we can often find large project codebases where the number of files has to be reduced at the cost of modularity. For instance, in some SSL/TLS libraries (e.g. OpenSSL, mbedTLS), we can often find cryptographic implementations concentrated in one single `.c/.h` file pair rather than spanned across many files.

The goal here is to have a glue code for extracting and combining together all the necessary code pieces of the CRYSTALS-Kyber reference implementation. The final output is given by the `kyber_fused.h` and `kyber_fused.c` pair containing all necessary code for implementing the (1) keypair generation, (2) encapsulation, and (3) decapsulation functionalities. In turn, these files can be integrated into larger codebases or quick testbeds with less effort when modifying the build flow.

### Usage

To generate `kyber_fused.h` and `kyber_fused.c` from Kyber sources:

```
python3 fuse.py
```

### Import Sequence

`kyber_fused.h`:
- `params.h` &rarr; `kem.h`

`kyber_fused.c`:
- `reduce.h` &rarr; `symmetric.h` &rarr; `poly.h` &rarr; `polyvec.h` &rarr; `symmetric-aes.c` &rarr; `symmetric-shake.c` &rarr; `reduce.c` &rarr; `ntt.c` &rarr; `cbd.c` &rarr; `poly.c` &rarr; `polyvec.c` &rarr; `incpa.c` &rarr; `verify.c` &rarr; `kem.c`

### Notes

- All the internal functions (i.e., all the ones except `crypto_kem_keypair`, `crypto_kem_enc`, `crypto_kem_dec` become static functions in `kyber_fused.c`).
- The extraction patterns in `extractors` might be applicable to other libraries (e.g. Dilithium), however the extraction rules in `fuse.py` (string matches, before/after occurrences) are very specific to Kyber. A future improvement could include more generalizable extractors.
