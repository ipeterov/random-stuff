def turtle(program):

    def indent(line):
        count = 0
        for char in line:
            if char == ' ':
                count += 1
            else:
                break
        return count

    def separate_loop(program, loop_index):
        beginning_indent = indent(program[loop_index + 1])
        for index, line in enumerate(program[loop_index + 2:]):
            if indent(line) < beginning_indent:
                return program[loop_index + 1: loop_index + index + 2]
        else:
            return program[loop_index + 1:]

    def eval_turtle(program, count):
        nonlocal x, y, painted

        for i in range(count):
            for index, line in enumerate(program):
                command = line.split()
                if len(command) == 1:
                    command = command[0]
                    print(command)
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
                    eval_turtle(separate_loop(program, index), int(command[1]) - 1)

    x, y = 0, 0
    painted = set()

    eval_turtle(program, 1)

    return painted

with open('program.turtle') as program_text:
    program = [line.strip('\n') for line in program_text.readlines()]

for elem in sorted(turtle(program));
    print(elem)
