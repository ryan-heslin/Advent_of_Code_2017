with open("inputs/day1.txt") as f:
    raw_input = f.read().rstrip("\n")

processed = list(map(int, raw_input))

part1 = sum(
    x if x == y else 0 for x, y in zip(processed, processed[1:] + [processed[0]])
)

print(part1)


length = len(processed)
half = length // 2
part2 = sum(x for i, x in enumerate(processed) if processed[(i + half) % length] == x)
print(part2)
