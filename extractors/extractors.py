def extract_lines_between(f_path, st_occurrence, end_occurrence):
    """
    This extracts all the lines between the first line containing the 'st_occurrence' and the first line
    containing the 'end_occurrence', including these occurrence lines
    :param f_path: path to source file
    :param st_occurrence: string marking the beginning of the extraction
    :param end_occurrence: string marking the end of the extraction
    :return: extracted relevant content
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


def extract_lines_excluding(f_path, str_undesired):
    """
    This extracts all the lines of the file except where the occurrences specified in str_undesired appear
    :param f_path: path to source file
    :param str_undesired: list of undesired string occurrences marking lines to be excluded
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if any(undesired in ln for undesired in str_undesired):
                continue
            else:
                content.append(ln)
        return content


def extract_lines_occurrences(f_path, str_desired):
    """
    This extracts all the lines of the file where the occurrences specified in str_undesired appear
    :param f_path: path to source file
    :param str_desired: list of desired string occurrences marking lines to be included
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if any(undesired in ln for undesired in str_desired):
                content.append(ln)
        return content
