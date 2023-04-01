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
    In this file we have to extract everything except the includes and the header defines
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

        # Function implementations
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
        # out_buf.append('\n//__KYBER_FUSE__: extracted from poly.c')
        # [out_buf.append(line) for line in extract_from_poly_c('kyber/ref/poly.c')]
        # out_buf.append('// end of poly.c\n')

        # ========================================== (FINAL) Write to file =============================================
        for line in out_buf:
            out_f.write(line)
