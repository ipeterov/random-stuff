def mysortfunc(key):
    ords = [ord(c) - 97 for c in key[0].lower()]
    ordsum = 0
    for i, o in enumerate(ords):
        ordsum += o / 25 ** (i + 1)
    return key[1] - ordsum

attempts = []
for i in range(1000):
    inp = input().split()
    if inp != ['stop']:
        attempts.append(inp)
    else:
        break

students = {}
for attempt in attempts:
    sucsess = attempt[-1]
    if sucsess == 'OK':
        language = attempt[-2]
        name = ' '.join(attempt[:3])
        task = attempt[3]
        if name not in students:
            students[name] = {language: {task}}
        else:
            if language not in students[name]:
                students[name][language] = {task}
            else:
                students[name][language].add(task)

languages = {}
for key in students:
    for language in students[key]:
        if language not in languages:
            languages[language] = len(students[key][language])
        else:
            languages[language] += len(students[key][language])

for elem in sorted(languages.items(), key = mysortfunc):
    print(elem[0], elem[1])
