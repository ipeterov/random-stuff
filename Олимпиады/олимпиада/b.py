colbs = []
for i in range(10):
    colbs.append(int(input()))

average = sum(colbs) / len(colbs)

count = 0
for colb in colbs:
    if colb > average:
        count += 1

print(count)
