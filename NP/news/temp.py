def censor(text: str):
    bad_words = ['fuck', 'shit', 'def', 'no', 'filter']
    ln = len(bad_words)
    censored_text = ''
    slice = ''
    mask = '*'
    for i in text:
        slice += i
        # print(slice)
        lower_slice = slice.lower()

        flag = 0
        for j in bad_words:
            if not lower_slice in j:
                flag += 1
            if lower_slice == j:
                censored_text += mask * len(slice)
                flag -= 1
                slice = ''

        if flag == ln:
            censored_text += slice
            slice = ''

    if lower_slice != '' and lower_slice not in bad_words:
        censored_text += slice
    elif lower_slice != '':
        censored_text += mask * len(slice)

    return censored_text


# text = "fds dfsd dsfd wetwe werwe fuck FUCKing a shit"

# print(censor(text))
