import re


def remove_cost(string):
    """remove the cost from the feedback message"""
    pattern = "\(cost=.+\)"
    replace = ''
    string = re.sub(pattern, replace, string)
    return string.strip()


def add_line_to_line_number(string):
    """adds 'at line number' before line number in the feedback message"""
    pattern = 'at (?=\d)'
    return re.sub(pattern, 'at line ', string)


#
def post_process_feedback(string):
    """
    splits the feedback message lines into sepearte lines.gets the index of the places where strings dont match.
    Adds carets underneath to highlight the nonmatching words
    """
    pattern = "('.*')\nto\n('.*')"
    array = string.split('\n')
    matches = re.findall(pattern, string)
    array2 = []
    array3 = []
    caret_strings = None
    for i in range(len(array)):
        array2.append(array[i])
        array3.append(array[i])
        if caret_strings is not None:
            array2.pop()
            array2.append(caret_strings)
            array3[-1] = l1
            caret_strings = None
        if i != 0 and array[i] == 'to':
            for match in matches:
                if array[i - 1] == match[0] and array[i + 1] == match[1]:
                    s, t = separate_brackets(match)
                    l1 = gen_first_level_hint(s, t)
                    s, t = generate_caret_strings((s, t))
                    array2.pop(-2)
                    array2.insert(-1, s)
                    caret_strings = t
    string = '\n'.join(array2)
    l1_string = '\n'.join(array3)
    return string, l1_string


def generate_caret_strings(match):
    """generate carets under nonmatching words:
    split the strings to arrays containing words and spaces
    checks if words in two strings are different and then generate caret strings to hightlight difference.
    It will generate caret for the words under the larger strings after it finishes iterateing both arrays by length.
    It generates careted strings to be placed under feedback message code strings
    """
    s, t = match
    arr1 = s.split()
    arr2 = t.split()
    sp1 = re.split(r'\S+', s)[1:]
    sp2 = re.split(r'\S+', t)[1:]
    cs1 = cs2 = ''
    for i, m in enumerate(zip(arr1, arr2)):
        if m[0] != m[1]:
            small = len(m[0]) if len(m[1]) > len(m[0]) else len(m[1])
            careted = False
            for j in range(small):
                if m[0][j] != m[1][j]:
                    cs1 += '^'
                    cs2 += '^'
                    careted = True
                    break
                else:
                    cs2 += ' '
                    cs1 += ' '
            cs1 += ' ' * (len(m[0]) - j - 1) + sp1[i] if careted else '^' + ' ' * (len(m[0]) - j - 2) + sp1[i]
            cs2 += ' ' * (len(m[1]) - j - 1) + sp2[i] if careted else '^' + ' ' * (len(m[0]) - j - 2) + sp1[i]
        else:
            cs1 += ' ' * len(m[0]) + sp1[i]
            cs2 += ' ' * len(m[1]) + sp2[i]
    arr, sp, cs = (arr1, sp1, cs1) if len(arr1) > len(arr2) else (arr2, sp2, cs2)
    arr, sp = arr[i + 1:], sp[i + 1:]
    for i in range(len(arr)):
        cs += '^' + ' ' * (len(arr[i]) - 1) + sp[i]
    if len(arr1) > len(arr2):
        return break_lines(s, t, cs, cs2)
    else:
        return break_lines(s, t, cs1, cs)


def break_lines(s, t, cs1, cs2):
    """break lines if line length would cause jupyter cell to overflow"""
    rs = rt = ''
    if len(s) < 111:
        return s + '\n' + cs1, t + '\n' + cs2
    else:
        for i in range(0, len(s), 110):
            rs += s[slice(i, 110 + i)] + '\n' + cs1[slice(i, 110 + i)] + '\n'
        for i in range(0, len(t), 110):
            rt += t[slice(i, 110 + i)] + '\n' + cs2[slice(i, 110 + i)] + '\n'

    return rs, rt


def separate_brackets(match):
    """helper function to separate pairs of brackets from comments in feedback message and not alter the ones that are
    part of codes and suggested fixes"""
    s, t = match
    s = s[1:-1]
    t = t[1:-1]
    bracket_pattern = "[\[\]\(\)\{\}]"
    m1 = re.search(bracket_pattern, s)
    m2 = re.search(bracket_pattern, t)
    if m1 or m2:
        string_pattern = "[\"']"
        m3 = re.search(string_pattern, s)
        m4 = re.search(string_pattern, t)
        if m3 or m4:
            if m3:
                s = gen_new_string(s)
            if m4:
                t = gen_new_string(t)
            return "'" + s + "'", "'" + t + "'"
        else:
            s = re.sub('[\[\(\{](?=\\S)+', lambda m: m.group(0) + ' ', s)
            s = re.sub('(?<=\\S)+[\]\)\}]', lambda m: " " + m.group(0), s)
            t = re.sub('[\[\(\{](?=\\S)+', lambda m: m.group(0) + ' ', t)
            t = re.sub('(?<=\\S)+[\]\)\}]', lambda m: " " + m.group(0), t)
            return "'" + s + "'", "'" + t + "'"
    else:
        return "'" + t + "'", "'" + t + "'"


def gen_new_string(s):
    """stitches up strings in code with original spaces preserved"""
    single_quote_indices = [x.start() for x in list(re.finditer('[\']', s))]
    double_quote_indices = [x.start() for x in list(re.finditer('["]', s))]
    escape_single_quote_indices = [x.start() for x in list(re.finditer('\\\\\'', '\\\'', s))]
    escape_double_quote_indices = [x.start() for x in list(re.finditer('\\\\"', '\\"', s))]
    string_indices = get_string_indices(single_quote_indices, double_quote_indices,
                                        escape_single_quote_indices,
                                        escape_double_quote_indices)
    counter = 0
    new_s = ''
    for pair in string_indices:
        if len(pair) == 1:
            first_sub = re.sub('[\[\(\{](?=\\S)+', lambda m: m.group(0) + ' ', s[counter:])
            new_s += re.sub('(?<=\\S)+[\]\)\}]', lambda m: " " + m.group(0), first_sub)
        else:
            f = pair[0]
            l = pair[1] + 1
            quote_sl = slice(f, l)
            not_quote_sl = slice(counter, f)
            first_sub = re.sub('[\[\(\{](?=\\S)+', lambda m: m.group(0) + ' ', s[not_quote_sl])
            new_s += re.sub('(?<=\\S)+[\]\)\}]', lambda m: " " + m.group(0), first_sub) + s[quote_sl]
            counter = l + 1
    s = new_s
    return s


def get_string_indices(single_quote_indices, double_quote_indices, escape_single_quote_indices,
                       escape_double_quote_indices):
    """gets indices of strings in the feedback messages after comparing quote symbol indices and escape quote indices"""
    string_indices = []

    while single_quote_indices or double_quote_indices:
        if single_quote_indices and double_quote_indices:
            if single_quote_indices[0] < double_quote_indices[0]:
                string_index_pair, single_quote_indices, double_quote_indices, escape_single_quote_indices, \
                escape_double_quote_indices = string_indices_generator(single_quote_indices, double_quote_indices,
                                                                       escape_single_quote_indices,
                                                                       escape_double_quote_indices)
                string_indices.append(string_index_pair)

            else:
                string_index_pair, double_quote_indices, single_quote_indices, escape_double_quote_indices, \
                escape_single_quote_indices = string_indices_generator(double_quote_indices, single_quote_indices,
                                                                       escape_double_quote_indices,
                                                                       escape_single_quote_indices)
                string_indices.append(string_index_pair)
        elif single_quote_indices:
            string_index_pair, single_quote_indices, _, escape_single_quote_indices, _ = \
                string_indices_generator(single_quote_indices, None, escape_single_quote_indices, None)
            string_indices.append(string_index_pair)
        elif double_quote_indices:
            string_index_pair, single_quote_indices, _, escape_single_quote_indices, _ = \
                string_indices_generator(double_quote_indices, None, escape_double_quote_indices, None)
            string_indices.append(string_index_pair)
    return string_indices


# generate indices for strings in codes
def string_indices_generator(indices, indices2, escape_indices, escape_indices2):
    """generates string indices of strings from quote indices arrays"""
    quote_pair = []
    if indices:
        v = indices.pop(0)
        quote_pair.append(v)
        if indices:
            n = indices.pop(0)
        else:
            return quote_pair, [], [], [], []
        if indices2:
            while indices2[0] < n:
                indices2.pop(0)
        if escape_indices:
            while escape_indices[0] + 1 <= n:
                e = escape_indices.pop(0)
                if e + 1 == n:
                    n = indices.pop(0)
        if escape_indices2:
            while escape_indices2[0] + 1 <= n:
                escape_indices2.pop(0)
        quote_pair.append(n)
    return quote_pair, indices, indices2, escape_indices, escape_indices2


# this function is not used in the current implementation of clippy yet
def gen_first_level_hint(s, t):
    """generates first level hint"""
    arr1 = s.split()
    arr2 = t.split()
    sp2 = re.split(r'\S+', t)[1:]
    string = ''
    for i, m in enumerate(zip(arr1, arr2)):
        if m[0] != m[1]:
            arr2[i] = '?'
    for i in range(len(arr2)):
        string += arr2[i] + sp2[i]
    return string


def postparse(string):
    """the main function that invokes all the function to make changes to feedback messages"""
    string = remove_cost(string)
    string = add_line_to_line_number(string)
    string, l1_string = post_process_feedback(string)
    # print(l1_string)
    return string
