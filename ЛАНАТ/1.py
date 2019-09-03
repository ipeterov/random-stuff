people = sorted([input().split() for i in range(int(input()))], key=lambda x: int(x[1]))
salaries = [int(x[1]) for x in people]

print(people[-1][0], people[-1][1])
print(people[0][0], people[0][1])
print(sum(salaries) / len(salaries))
