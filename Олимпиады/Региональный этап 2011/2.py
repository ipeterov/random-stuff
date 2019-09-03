n = int(input())

digits = '0123456789'
scnumbers = {}
for i in range(n):
    school = input()
    scnumber = ''
    for char in school:
        if char in digits:
            scnumber += char
    scnumber = int(scnumber)
    if scnumber in scnumbers:
        scnumbers[scnumber] += 1
    else:
        scnumbers[scnumber] = 1

for key in scnumbers.copy():
    if scnumbers[key] > 5:
        del scnumbers[key]

print(len(scnumbers))
for key in scnumbers:
    print(key)
