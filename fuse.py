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


if __name__ == '__main__':
    # Create kyber_fused.h header file
    with open('output/kyber_fused.h', 'w') as out_f:
        # Load contents from params.h
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

        # Write to file
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
        # Load contents from reduce.h
        out_buf.append('\n//__KYBER_FUSE__: extracted from reduce.h\n')
        [out_buf.append(line) for line in extract_from_reduce_h('kyber/ref/reduce.h')]
        out_buf.append('// end of reduce.h\n')

        # Load contents from reduce.c
        out_buf.append('\n//__KYBER_FUSE__: extracted from reduce.c')
        [out_buf.append(line) for line in extract_from_reduce_c('kyber/ref/reduce.c')]
        out_buf.append('// end of reduce.c\n')

        # Append 'static' to the functions from reduce.c
        ins_idx = out_buf.index('int16_t montgomery_reduce(int32_t a)\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        ins_idx = out_buf.index('int16_t barrett_reduce(int16_t a) {\n')
        out_buf.insert(ins_idx, 'KYBERFUSE_STATIC ')

        # Load contents from ntt.c
        out_buf.append('\n//__KYBER_FUSE__: extracted from ntt.c')
        [out_buf.append(line) for line in extract_from_ntt_c('kyber/ref/ntt.c')]
        out_buf.append('// end of ntt.c\n')

        # Write to file
        for line in out_buf:
            out_f.write(line)
