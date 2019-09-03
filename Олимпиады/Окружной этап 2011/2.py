colbs = []
for i in range(10):
    colbs.append(int(input()))
av = sum(colbs) / 10
counter = 0
for i in range(10):
    if colbs[i] > av:
        counter += 1
print(counter)
