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


def solve_part2(instructions):

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
            i += registers.get(y, y) if registers.get(x, x) > 0 else 1
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

        while 0 <= i < length:
            args = instructions[i]
            if args[0] == "snd":
                i += 1
                sent[initial] += 1
                yield registers.get(args[1], args[1])
            # Yield values at first "rcv"
            elif args[0] == "rcv":
                i += 1
                new_val = yield True
                registers[args[1]] = new_val

            else:
                i = mapping[args[0]](*args[1:], i)
        yield False

    program0 = program(0)
    program1 = program(1)
    programs = {
        0: {"program": program0, "queue": deque([]), "exhausted": False, "last": 0},
        1: {"program": program1, "queue": deque([]), "exhausted": False, "last": 0},
    }

    while True:

        iterations = 0
        first = True
        while not programs[0]["exhausted"]:
            if type(programs[0]["last"]) == int:
                if not first:
                    programs[1]["queue"].appendleft(programs[0]["last"])
                programs[0]["last"] = next(programs[0]["program"])
            else:
                if not programs[0]["last"]:
                    programs[0]["exhausted"] = True
                    break
                if len(programs[0]["queue"]):
                    programs[0]["last"] = programs[0]["program"].send(
                        programs[0]["queue"].pop()
                    )
                else:
                    break
            iterations += 1
            first = False

        first = True
        while True:
            if type(programs[1]["last"]) == int:
                if not first:
                    programs[0]["queue"].appendleft(programs[1]["last"])
                programs[1]["last"] = next(programs[1]["program"])
            else:
                if not programs[1]["last"]:
                    return sent[1]
                if len(programs[1]["queue"]):
                    programs[1]["last"] = programs[1]["program"].send(
                        programs[1]["queue"].pop()
                    )
                else:
                    break
            iterations += 1
            first = False

        if iterations == 0:
            return sent[1]


with open("inputs/day18.txt") as f:
    raw_input = f.read().splitlines()

instructions = [parse(line) for line in raw_input]
part1, mapping = recover(instructions)
print(part1)

part2 = solve_part2(instructions)
print(part2)
