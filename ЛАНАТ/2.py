n, k = [int(x) for x in input().split()]
times = []
for i in range(n):
    times.append(int(input()))

print(times[k-1] - times[k-2])
