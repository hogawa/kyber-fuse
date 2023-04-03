def extract_lines_between(f_path, st_occurrence, end_occurrence):
    """
    This extracts all the lines between the first line containing the 'st_occurrence' and the first line
    containing the 'end_occurrence', including these occurrence lines

    :param f_path:
    :param st_occurrence:
    :param end_occurrence:
    :return:
    """
    content = []
    extract = False
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if st_occurrence in ln:
                extract = True
            if extract:
                content.append(ln)
            if end_occurrence in ln:
                break
        return content
