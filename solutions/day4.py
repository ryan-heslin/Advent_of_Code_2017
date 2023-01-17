import re

with open("inputs/day4.txt") as f:
    raw_input = f.read().splitlines()

part1 = sum((not bool(re.match(r".*\b(\w+).*\b\1\b.*", line)) for line in raw_input))
print(part1)

part2 = 0
for line in raw_input:
    words = tuple(tuple(sorted(word)) for word in line.split(" "))
    part2 += len(set(words)) == len(words)

print(part2)
