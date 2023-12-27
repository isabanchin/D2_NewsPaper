from django import template

# если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(
register = template.Library()


# регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
@register.filter(name='multiply')
def multiply(value, arg):
    # проверяем, что value -- это точно строка, а arg -- точно число, чтобы не возникло курьёзов
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        # в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')


@register.filter(name='censor')
def censor(text: str):
    bad_words = ['fuck', 'shit', 'def', 'no', 'filter']
    ln = len(bad_words)
    censored_text = ''
    bit = ''
    mask = '*'
    for i in text:
        bit += i
        print(bit)
        lower_slice = bit.lower()
        flag = 0
        for j in bad_words:
            if not lower_slice in j:
                flag += 1
            if lower_slice == j:
                censored_text += mask * len(bit)
                flag -= 1
                bit = ''
        if flag == ln:
            censored_text += bit
            bit = ''
    if lower_slice != '' and lower_slice not in bad_words:
        censored_text += bit
    elif lower_slice != '':
        censored_text += mask * len(bit)
    return censored_text
