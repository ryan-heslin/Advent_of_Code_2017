from collections import defaultdict
from collections import deque


def is_number(x):
    return x[0] == "-" or x.isnumeric()


def parse(line):
    parts = line.split(" ")
    parts[1:] = [int(part) if is_number(part) else part for part in parts[1:]]
    return parts


def recover(instructions):
    registers = defaultdict(lambda: 0)
    frequency = []
    part1 = []
    i = 0
    length = len(instructions)

    def snd(x, i):
        nonlocal frequency
        frequency.append(registers.get(x, x))
        return i + 1

    def set(x, y, i):
        registers[x] = registers.get(y, y)
        return i + 1

    def add(x, y, i):
        registers[x] += registers.get(y, y)
        return i + 1

    def mul(x, y, i):
        registers[x] *= registers.get(y, y)
        return i + 1

    def mod(x, y, i):
        registers[x] %= registers.get(y, y)
        return i + 1

    def rcv(x, i):
        nonlocal part1
        nonlocal frequency
        if registers.get(x, x) != 0:
            part1.append(frequency[-1])
        return i + 1

    def jgz(x, y, i):
        i += registers.get(y, y) if registers[x] > 0 else 1
        return i

    mapping = {
        "snd": snd,
        "set": set,
        "add": add,
        "mul": mul,
        "mod": mod,
        "rcv": rcv,
        "jgz": jgz,
    }

    while not part1 and 0 <= i < length:
        args = instructions[i]
        i = mapping[args[0]](*args[1:], i)

    return part1[0], mapping


def part2(instructions):

    length = len(instructions)
    sent = {0: 0, 1: 0}

    def program(initial):
        def set(x, y, i):
            registers[x] = registers.get(y, y)
            return i + 1

        def add(x, y, i):
            registers[x] += registers.get(y, y)
            return i + 1

        def mul(x, y, i):
            registers[x] *= registers.get(y, y)
            return i + 1

        def mod(x, y, i):
            registers[x] %= registers.get(y, y)
            return i + 1

        def jgz(x, y, i):
            i += registers.get(y, y) if registers[x] > 0 else 1
            return i

        mapping = {
            "set": set,
            "add": add,
            "mul": mul,
            "mod": mod,
            "jgz": jgz,
        }
        nonlocal sent
        nonlocal instructions
        nonlocal length
        i = 0
        registers = defaultdict(lambda: 0)
        registers["p"] = initial
        output = deque([])
        input = deque([])

        while 0 <= i < length:
            args = instructions[i]
            # print(args)
            # print(dict(registers))
            if args[0] == "snd":
                i += 1
                sent[initial] += 1
                output.appendleft(registers.get(args[1], args[1]))
            # Yield values at first "rcv"
            elif args[0] == "rcv":
                i += 1
                if len(input) == 0:
                    yield from output.copy()
                    input = yield
                    output = deque([])
                registers[args[1]] = input.pop()

            else:
                i = mapping[args[0]](*args[1:], i)
        yield None

    program0 = program(0)
    program1 = program(1)

    while True:
        for_1 = next(program0)
        for_0 = next(program1)
        # No data available yet
        if for_0 is None or for_1 is None or not (len(for_0) or len(for_1)):
            break
        if len(for_0):
            print("for_0")
            print(for_0)
            print("\n")
            program0.send(for_0)
        if len(for_1):
            print("for_1")
            print(for_1)
            print("\n")
            program1.send(for_1)

    return sent[1]


with open("inputs/day18.txt") as f:
    raw_input = f.read().splitlines()

instructions = [parse(line) for line in raw_input]
part1, mapping = recover(instructions)
print(part1)

part2 = part2(instructions)
print(part2)

# TODO ensure functions can actually write registers
