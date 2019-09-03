def remake(number):
    newnumber = ''
    allowed = ['1','2','3','4','5','6','7','8','9','0','+']
    for char in number:
        if char in allowed:
            newnumber += char
    newnumber = newnumber.replace('+7', '8')
    if len(newnumber) == 7:
        newnumber = '8495' + newnumber
    return newnumber
    
orig = remake(input())
numbers = []
for i in range(3):
    numbers.append(remake(input()))
for number in numbers:
    if number == orig:
        print('YES')
    else:
        print('NO')
