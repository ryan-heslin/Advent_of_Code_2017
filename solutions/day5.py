with open("inputs/day5.txt") as f:
    raw_input = f.read().splitlines()

processed = [int(x) for x in raw_input]

lower = pos = steps = 0
upper = len(processed) - 1
while lower <= pos <= upper:
    if processed[pos] == 0:
        processed[pos] += 1
    else:
        old_pos = pos
        pos += processed[old_pos]
        processed[old_pos] += 1
    steps += 1

print(steps)

processed = [int(x) for x in raw_input]
lower = pos = steps = 0
upper = len(processed) - 1
while lower <= pos <= upper:
    if processed[pos] == 0:
        processed[pos] += 1
    else:
        old_pos = pos
        pos += processed[old_pos]
        processed[old_pos] += -1 if processed[old_pos] >= 3 else 1
    steps += 1
print(steps)
