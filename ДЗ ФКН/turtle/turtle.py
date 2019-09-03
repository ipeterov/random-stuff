def indent(line):
    count = 0
    for char in line:
        if char == ' ':
            count += 1
        else:
            break



def eval_turtle(program):

    def return_to_stack():
        if stack[-1]['count'] != 0:
            index = stack[-1]['index']
            stack[-1]['count'] -= 1
        else:
            del stack[-1]
            return_to_stack()

    x, y = 0, 0
    painted = set()
    stack = []

    index = 0
    while True:
        if index != 0 and indent(program[index]) < indent(program[index-1]):
            return_to_stack()
            continue

        command = program[index].split()

        if len(command) == 1:
            command = command[0]
            if command == 'left':
                x -= 1
            elif command == 'right':
                x += 1
            elif command == 'down':
                y -= 1
            elif command == 'up':
                y += 1
            elif command == 'paint':
                painted.add((x, y))
        else:
            if command[0] == 'loop':
                stack.append({'index': index + 1, 'count': int(command[1])})

