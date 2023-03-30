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


if __name__ == '__main__':
    # Create kyber_fused.h header file
    with open('output/kyber_fused.h', 'w') as out_f:
        # Load contents from params.h
        out_buf = extract_from_params_h('kyber/ref/params.h')

        # Insert include statements right after header define
        includes = (
            '\n'
            '//__KYBER_FUSE__\n'
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
        # out_f.write('#include "kyber_fused.h"')
        includes = (
            '#include "kyber_fused.h"\n'
        )
        out_buf.append(includes)

        # Load contents from reduce.h
        out_buf.append('\n//__KYBER_FUSE__: extracted from reduce.h\n')
        for line in extract_from_reduce_h('kyber/ref/reduce.h'):
            out_buf.append(line)

        # Write to file
        for line in out_buf:
            out_f.write(line)
