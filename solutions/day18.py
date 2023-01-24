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

        while 0 <= i < length:
            args = instructions[i]
            # print(args)
            # print(dict(registers))
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
        0: {"program": program0, "queue": deque([]), "exhausted": False},
        1: {"program": program1, "queue": deque([]), "exhausted": False},
    }

    # Run both to first receive
    while not programs[0]["exhausted"]:
        new_value = next(programs[0]["program"])
        if type(new_value) == int:
            programs[1]["queue"].appendleft(new_value)
        else:
            if not new_value:
                programs[0]["exhausted"] = True
            break

    while True:
        new_value = next(programs[1]["program"])
        if type(new_value) == int:
            programs[1]["queue"].appendleft(new_value)
        else:
            if not new_value:
                return sent[1]
            break

    while True:
        # Run until needs data
        # False means program completed
        print(programs)
        # Deadlock - no data available
        if not (programs[0]["queue"] or programs[1]["queue"]):
            return sent[1]

        print(programs)
        next_value = True
        while programs[1]["queue"]:
            # Receiving new value
            if type(next_value) == int:
                # Sending new value
                programs[0]["queue"].appendleft(next_value)
                next_value = next(programs[1]["program"])
            else:
                if next_value:
                    next_value = programs[1]["program"].send(programs[1]["queue"].pop())
                else:
                    return sent[1]

        print(programs[0])
        if not programs[0]["exhausted"]:
            next_value = True
            while programs[0]["queue"]:
                if type(next_value) == int:
                    # Sending new value
                    programs[1]["queue"].appendleft(next_value)
                    next_value = next(programs[0]["program"])
                else:
                    if next_value:
                        next_value = programs[0]["program"].send(
                            programs[0]["queue"].pop()
                        )
                    else:
                        programs[0]["exhausted"] = True
                        break
        print("---------------")
        # breakpoint()


with open("inputs/day18.txt") as f:
    raw_input = f.read().splitlines()

instructions = [parse(line) for line in raw_input]
part1, mapping = recover(instructions)
print(part1)

part2 = part2(instructions)
print(part2)

# TODO ensure functions can actually write registers
# 132 too low
