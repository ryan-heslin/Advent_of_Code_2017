import utils.knot_hash as kh


with open("inputs/day10.txt") as f:
    raw_input = f.read()

lengths = list(map(int, raw_input.split(",")))

n = 256
hashed = kh.knot_hash(lengths, n)
part1 = hashed[0] * hashed[1]
print(part1)

part2 = kh.complete_hash(raw_input.rstrip("\n").lstrip("\n"), n=n, rounds=64)
print(part2)
