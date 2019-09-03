# def find_mixes(l, r): # l - длина списка, r - остаток
    # if l == 1:
        # return [[r]]
    # else:
        # mixes = []
        # for i in range(r + 1):
            # mixes.extend(([i] + x for x in find_mixes(l - 1, r - i)))
        # return mixes


def find_mixes(l, r):  # l - длина списка, r - остаток
    if l == 1:
        return [[r]]
    else:
        return (y for i in range(r + 1) for y in ([i] + x for x in find_mixes(l - 1, r - i)))


def apply_mix(word1, word2, mix):
    res = word2[:mix[0]]
    ci = 0
    for i in range(len(word1)):
        ci += mix[i]
        res += word1[i] + word2[ci:ci + mix[i + 1]]
    return res

word1, word2 = input().split()

uniques = set((apply_mix(word1, word2, mix)
               for mix in find_mixes(len(word1) + 1, len(word2))))

for elem in uniques:
    print(elem)
