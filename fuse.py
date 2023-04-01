def extract_from_params_h(f_path):
    with open(f_path, 'r') as in_f:
        content = [ln for ln in in_f]
        return content


def extract_from_reduce_h(f_path):
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if 'MONT' in ln:
                content.append(ln)
            if 'QINV' in ln:
                content.append(ln)
        return content


def extract_from_symmetric_h(f_path):
    """
    In this file we have to extract everything except the includes, the header defines, and the function skelektons
    :param f_path: path to symmetric.h file
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        go = False  # This is to remove the initial empty lines
        for ln in in_f:
            if 'KYBER_90S' in ln:
                go = True  # From here on, we can start extracting lines
            if go:
                if 'SYMMETRIC_H' not in ln and \
                        '#include <stddef.h>' not in ln and \
                        '#include <stdint.h>' not in ln and \
                        'void' not in ln and \
                        'const uint8_t seed[KYBER_SYMBYTES],' not in ln and \
                        'uint8_t x,' not in ln and \
                        'uint8_t y);' not in ln and \
                        '#include "params.h"' not in ln:
                    content.append(ln)
            if '#endif /* KYBER_90S */' in ln:
                go = False  # Stop extraction here to avoid blank line
        return content


def extract_from_poly_h(f_path):
    """
    In this file we just have to extract the definition of the 'poly' struct
    :param f_path: path to source poly.h file
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        found = False
        for ln in in_f:
            if "typedef struct" in ln:
                found = True
                content.append(ln)
            elif found:
                content.append(ln)
                if "poly;" in ln:
                    break
        return content


def extract_from_polyvec_h(f_path):
    """
    In this file we just have to extract the definition of the 'polyvec' struct
    :param f_path: path to source polyvec.h file
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        found = False
        for ln in in_f:
            if "typedef struct" in ln:
                found = True
                content.append(ln)
            elif found:
                content.append(ln)
                if "polyvec;" in ln:
                    break
        return content


def extract_from_symmetric_aes_c(f_path):
    """

    :param f_path:
    :return:
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if "#include" not in ln:
                content.append(ln)
        return content


def extract_from_symmetric_shake_c(f_path):
    """

    :param f_path:
    :return:
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if "#include" not in ln:
                content.append(ln)
        return content


def extract_from_reduce_c(f_path):
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if "#include" not in ln:
                content.append(ln)
        return content


def extract_from_ntt_c(f_path):
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if "#include" not in ln:
                content.append(ln)
        return content


def extract_from_cbd_c(f_path):
    """
    In this file we can extract everything, except the '#include' statements
    :param f_path: path to source cbd.c file
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if "#include" not in ln:
                content.append(ln)
        return content


def extract_from_poly_c(f_path):
    """
    In this file we can extract everything, except the '#include' statements
    :param f_path: path to source poly.c file
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if "#include" not in ln:
                content.append(ln)
        return content


def extract_from_polyvec_c(f_path):
    """
    In this file we can extract everything, except the '#include' statements
    :param f_path: path to source polyvec.c file
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if "#include" not in ln:
                content.append(ln)
        return content


if __name__ == '__main__':
    # Create kyber_fused.h header file
    with open('output/kyber_fused.h', 'w') as out_f:
        # ======================================== Load contents from params.h =========================================
        out_buf = extract_from_params_h('kyber/ref/params.h')

        # Insert include statements right after header define
        includes = (
            '\n'
            '//__KYBER_FUSE__: common includes\n'
            '#include <stdint.h>\n'
            '#include <stddef.h>\n'
            '#include <string.h>\n'
        )
        ins_idx = out_buf.index('#define PARAMS_H\n') + 1
        out_buf.insert(ins_idx, includes)

        # =========================================== (FINAL) Write to file ============================================
        for line in out_buf:
            out_f.write(line)

    # Create kyber_fused.c implementation file
    out_buf = []
    with open('output/kyber_fused.c', 'w') as out_f:
        # Include statements
        includes = (
            '#include "kyber_fused.h"\n'
        )
        out_buf.append(includes)

        # Local definitions
        out_buf.append('\n#define KYBERFUSE_STATIC static\n')

        # Internal parameters
        # ====================================== Load contents from reduce.h ===========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from reduce.h\n')
        [out_buf.append(line) for line in extract_from_reduce_h('kyber/ref/reduce.h')]
        out_buf.append('// end of reduce.h\n')

        # ===================================== Load contents from symmetric.h =========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from symmetric.h\n')
        [out_buf.append(line) for line in extract_from_symmetric_h('kyber/ref/symmetric.h')]
        out_buf.append('// end of symmetric.h\n')

        # Structs and common variables
        # ======================================= Load contents from poly.h ============================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from poly.h\n')
        [out_buf.append(line) for line in extract_from_poly_h('kyber/ref/poly.h')]
        out_buf.append('// end of poly.h\n')

        # ===================================== Load contents from polyvec.h ===========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from polyvec.h\n')
        [out_buf.append(line) for line in extract_from_polyvec_h('kyber/ref/polyvec.h')]
        out_buf.append('// end of polyvec.h\n')

        # Function implementations
        # ===================================== Load contents from symmetric-aes.c =====================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from symmetric-aes.c\n')
        out_buf.append('#ifdef KYBER_90S')
        [out_buf.append(line) for line in extract_from_symmetric_aes_c('kyber/ref/symmetric-aes.c')]
        out_buf.append('#endif  /* KYBER_90S */\n')
        out_buf.append('// end of symmetric-aes.c\n')

        # Append 'static' to the functions from symmetric-aes.c
        ins_idx = out_buf.index('void kyber_aes256xof_absorb(aes256ctr_ctx *state, const uint8_t seed[32], '
                                'uint8_t x, uint8_t y)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void kyber_aes256ctr_prf(uint8_t *out, size_t outlen, const uint8_t key[32], '
                                'uint8_t nonce)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # ==================================== Load contents from symmetric-shake.c ====================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from symmetric-shake.c')
        [out_buf.append(line) for line in extract_from_symmetric_shake_c('kyber/ref/symmetric-shake.c')]
        out_buf.append('// end of symmetric-shake.c\n')

        # Append 'static' to the functions from symmetric-shake.c
        ins_idx = out_buf.index('void kyber_shake128_absorb(keccak_state *state,\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void kyber_shake256_prf(uint8_t *out, size_t outlen, const uint8_t key['
                                'KYBER_SYMBYTES], uint8_t nonce)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # ======================================== Load contents from reduce.c =========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from reduce.c')
        [out_buf.append(line) for line in extract_from_reduce_c('kyber/ref/reduce.c')]
        out_buf.append('// end of reduce.c\n')

        # Append 'static' to the functions from reduce.c
        ins_idx = out_buf.index('int16_t montgomery_reduce(int32_t a)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('int16_t barrett_reduce(int16_t a) {\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # ========================================= Load contents from ntt.c ===========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from ntt.c')
        [out_buf.append(line) for line in extract_from_ntt_c('kyber/ref/ntt.c')]
        out_buf.append('// end of ntt.c\n')

        # Append static to zeta table and ntt.c functions
        ins_idx = out_buf.index('const int16_t zetas[128] = {\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void ntt(int16_t r[256]) {\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void invntt(int16_t r[256]) {\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void basemul(int16_t r[2], const int16_t a[2], const int16_t b[2], int16_t zeta)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # ========================================== Load contents from cbd.c ==========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from cbd.c')
        [out_buf.append(line) for line in extract_from_cbd_c('kyber/ref/cbd.c')]
        out_buf.append('// end of cbd.c\n')

        # Append static to cbd.c functions
        ins_idx = out_buf.index('void poly_cbd_eta1(poly *r, const uint8_t buf[KYBER_ETA1*KYBER_N/4])\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_cbd_eta2(poly *r, const uint8_t buf[KYBER_ETA2*KYBER_N/4])\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # ========================================= Load contents from poly.c ==========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from poly.c\n')
        out_buf.append('KYBERFUSE_STATIC void poly_reduce(poly *r);  // HSO: workaround since this is called before '
                       'the implementation\n')
        [out_buf.append(line) for line in extract_from_poly_c('kyber/ref/poly.c')]
        out_buf.append('// end of poly.c\n')

        # Append static to poly.c functions
        ins_idx = out_buf.index('void poly_compress(uint8_t r[KYBER_POLYCOMPRESSEDBYTES], const poly *a)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_decompress(poly *r, const uint8_t a[KYBER_POLYCOMPRESSEDBYTES])\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_tobytes(uint8_t r[KYBER_POLYBYTES], const poly *a)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_frombytes(poly *r, const uint8_t a[KYBER_POLYBYTES])\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_frommsg(poly *r, const uint8_t msg[KYBER_INDCPA_MSGBYTES])\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_tomsg(uint8_t msg[KYBER_INDCPA_MSGBYTES], const poly *a)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_getnoise_eta1(poly *r, const uint8_t seed[KYBER_SYMBYTES], uint8_t nonce)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_getnoise_eta2(poly *r, const uint8_t seed[KYBER_SYMBYTES], uint8_t nonce)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_ntt(poly *r)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_invntt_tomont(poly *r)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_basemul_montgomery(poly *r, const poly *a, const poly *b)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_tomont(poly *r)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_reduce(poly *r)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_add(poly *r, const poly *a, const poly *b)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void poly_sub(poly *r, const poly *a, const poly *b)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # ======================================= Load contents from polyvec.c =========================================
        out_buf.append('\n//__KYBER_FUSE__: extracted from polyvec.c')
        [out_buf.append(line) for line in extract_from_polyvec_c('kyber/ref/polyvec.c')]
        out_buf.append('// end of polyvec.c\n')

        # Append static to kyber_fused.c functions
        ins_idx = out_buf.index('void polyvec_compress(uint8_t r[KYBER_POLYVECCOMPRESSEDBYTES], const polyvec *a)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_decompress(polyvec *r, const uint8_t a[KYBER_POLYVECCOMPRESSEDBYTES])\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_tobytes(uint8_t r[KYBER_POLYVECBYTES], const polyvec *a)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_frombytes(polyvec *r, const uint8_t a[KYBER_POLYVECBYTES])\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_ntt(polyvec *r)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_invntt_tomont(polyvec *r)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_basemul_acc_montgomery(poly *r, const polyvec *a, const polyvec *b)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_reduce(polyvec *r)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('void polyvec_add(polyvec *r, const polyvec *a, const polyvec *b)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # ========================================== (FINAL) Write to file =============================================
        for line in out_buf:
            out_f.write(line)
