import sys

lines = []
for i in range(100):
    try:
        lines.append(input())
    except EOFError:
        break

output = ''

if '-l' in sys.argv:
    output += str(len(lines) + 1) + ' '

if '-w' in sys.argv:
    output += str(len(' '.join(lines).split())) + ' '

if '-m' in sys.argv:
    output += str(len(''.join(lines)) + len(lines)) + ' '

if '-L' in sys.argv:
    output += str(max((len(x) for x in lines)))

print(output)
