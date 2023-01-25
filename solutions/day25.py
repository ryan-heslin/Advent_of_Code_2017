from collections import defaultdict


def parse(chunks):
    moves = {"left": -1, "right": 1}
    opening = chunks[0].split("\n")
    begin_state = opening[0].rstrip(".")[-1]
    steps = int(opening[1].split(" ")[-2])
    result = {}

    for chunk in chunks[1:]:
        chunk = chunk.split("\n")
        state = chunk[0].rstrip(":")[-1]
        chunk.pop(0)
        this_chunk = {}
        for i in range(0, len(chunk) - 1, 4):
            current = chunk[i : (i + 4)]
            case = int(current[0].rstrip(":")[-1])
            write = int(current[1].rstrip(".")[-1])
            move = moves[current[2].split(" ")[-1].rstrip(".")]
            new_state = current[3].rstrip(".")[-1]
            this_chunk[case] = {"write": write, "move": move, "state": new_state}
        result[state] = this_chunk
    return result, begin_state, steps


with open("inputs/day25.txt") as f:
    raw_input = f.read().split("\n\n")

tape = defaultdict(lambda: 0)
program, begin_state, steps = parse(raw_input)

state = begin_state
position = 0

for _ in range(steps):
    value = tape[position]
    instructions = program[state][value]
    tape[position] = instructions["write"]
    position += instructions["move"]
    state = instructions["state"]

part1 = sum(tape.values())
print(part1)
