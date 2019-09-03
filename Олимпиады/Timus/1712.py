def turnback(reshetka):
    return [
    [reshetka[3][0],reshetka[3][1],reshetka[3][2],reshetka[3][3]],
    [reshetka[2][0],reshetka[2][1],reshetka[2][2],reshetka[2][3]],
    [reshetka[1][0],reshetka[1][1],reshetka[1][2],reshetka[1][3]],
    [reshetka[0][0],reshetka[0][1],reshetka[0][2],reshetka[0][3]]
    ]

reshetka = []
for x in range(4):
    reshetka.append(list(input()))
print(reshetka)
print(turnback(reshetka))

#letters = []
#for x in range(4):
    #letters.append(list(input()))

#password = ''
#for i in range(4):
    #print(reshetka)
    #reshetka = turnback(reshetka)
    #for x in range(4):
        #for y in range(4):
            #if reshetka[x][y] != '.':
                #password += letters[x][y]

#print(password)
