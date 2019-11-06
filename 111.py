def words_gen(word):

    def gen_words(sl, sr):
        while sl < len(signs):
            while sr < len(signs):
                genwords.extend([signs[sl] + word + signs[sr], word + signs[sr], signs[sl] + word])
                sr += 1
                sl += 1
                gen_words(sl, sr)

    signs = r".,:;-?!()[]\'’ "
    genwords = []

    gen_words(0, 0)

    return genwords


wg = words_gen("бот")
print(wg)
print(len(wg))


# a = 2
# b = c = 3
#
# f = [1,2,3,4,5]
# g = f
#
# print(type(a))
# print(type(b))
# print(type(c))
# print(type(f))
# print(g)
#
# AB = [1,2,3,4,5,7,0,9,12,4,2,7,8]
# print([x**2 for x in AB if x%2 == 0])
#
# cv = 2
# print('ok' if cv == 6 else 'not ok')
# print(cv)

# import re
# st = "(      *E ь^&12 + y   гд )"
# st = re.sub("^\s+|\s+|\s+$", "", st)
# st1 = re.sub("[^a-z0-9абвгдеёжзийклмнопрстуфхцчшщъьыэюя\\+]", "", st)
# print(st1)
# print(re.sub(r"^0-9", "", st))
# print(st)

# st = "https://cloud.(m)e?^"
# url = re.sub("[^a-zA-Z0-9:%./]", "", st)
# print(url)

# print(__name__)

