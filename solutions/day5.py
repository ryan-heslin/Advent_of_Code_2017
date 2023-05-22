def step(processed, change):
    processed = list(processed)
    lower = pos = steps = 0
    upper = len(processed) - 1
    while lower <= pos <= upper:
        if processed[pos] == 0:
            processed[pos] += 1
        else:
            old_pos = pos
            pos += processed[old_pos]
            processed[old_pos] += change(processed[old_pos])
        steps += 1

    return steps


with open("inputs/day5.txt") as f:
    raw_input = f.read().splitlines()

processed = list(map(int, raw_input))
one = lambda *_: 1
change = lambda x: -1 if x >= 3 else 1
part1 = step(processed, one)
part2 = step(processed, change)
print(part1)
print(part2)
