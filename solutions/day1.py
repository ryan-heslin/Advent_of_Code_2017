with open("inputs/day1.txt") as f:
    raw_input = f.read().rstrip("\n")

processed = [int(x) for x in raw_input]

part1 = sum(
    x if x == y else 0 for x, y in zip(processed, processed[1:] + [processed[0]])
)

length = len(processed)
half = length // 2
print(part1)

part2 = sum(
    x if processed[(i + half) % length] == x else 0 for i, x in enumerate(processed)
)
print(part2)
