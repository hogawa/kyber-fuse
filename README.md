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
