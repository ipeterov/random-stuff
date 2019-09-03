n = int(input())

tasks = []
for i in range(n):
    tasks.append([int(x) for x in input().split()])

tasks.sort()
contexts = []
context_creating = 0
for i in range(len(tasks)-1):

    if tasks[-1][2] > tasks[i+1][0]:
        if context_creating:
            contexts[-1][1] = i+1
            if tasks[i+1][0] + tasks[i+1][1] > contexts[-1][2]:
                contexts[-1][2] = tasks[i+1][0] + tasks[i+1][1] - 1
        else:
            context_creating = 1
            contexts.append([i, i+1, max(tasks[i][0] + tasks[i][1], tasks[i+1][0] + tasks[i+1][1]) - 1])
    else:
        context_creating = 0

print(contexts)

#for context in contexts:
    #context = list(range(*context))
    #variants = []
    #i = context[0]
    #while 1:
        #if not context:
            #break
        #for j in range(i, context[-1]):

        #i += 1
