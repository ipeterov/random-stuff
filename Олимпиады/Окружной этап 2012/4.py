packed = input()

codes = []
for i in range(0, len(packed), 2):
    codes.append(packed[i:i+2])

result = ''
for code in codes:
    q = int(code[0])
    result += code[1] * q

print(result)
