n = int(input())

for y in range(1,n+1):
    x = (n * y**3)**(0.5)
    if type(x) == float and int(x) == x:
        print(int(x))
        print(y)
        break
