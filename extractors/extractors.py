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


def extract_lines_excluding(f_path, undesired_list):
    """
    This extracts all the lines of the file except where the occurrences specified in str_undesired appear
    :param f_path: path to source file
    :param undesired_list: list of undesired string occurrences marking lines to be excluded
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if any(undesired in ln for undesired in undesired_list):
                continue
            else:
                content.append(ln)
        return content


def extract_lines_occurrences(f_path, desired_list):
    """
    This extracts all the lines of the file where the occurrences specified in str_undesired appear
    :param f_path: path to source file
    :param desired_list: list of desired string occurrences marking lines to be included
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        for ln in in_f:
            if any(desired in ln for desired in desired_list):
                content.append(ln)
        return content


def extract_lines_between_excluding(f_path, st_occurrence, end_occurrence, undesired_list):
    """
    This is a combination of extract_lines_between and extract_lines_excluding
    :param f_path: path to source file
    :param st_occurrence: string marking the beginning of the extraction
    :param end_occurrence: end_occurrence: string marking the end of the extraction
    :param undesired_list: list of undesired string occurrences marking lines to be excluded
    :return: extracted relevant content
    """
    content = []
    with open(f_path, 'r') as in_f:
        extract = False
        for ln in in_f:
            if st_occurrence in ln:
                extract = True
            if extract and not any(undesired in ln for undesired in undesired_list):
                content.append(ln)
            if end_occurrence in ln:
                break
        return content
