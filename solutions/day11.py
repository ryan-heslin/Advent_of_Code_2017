from functools import cache

with open("inputs/day11.txt") as f:
    raw_input = f.read().rstrip("\n")

# Coordinate system from https://www.redblobgames.com/grids/hexagons/

directions = raw_input.split(",")


@cache
def hex_manhattan(coord):
    s = -coord.real - coord.imag
    return int(abs(coord.real) + abs(coord.imag) + abs(s))


# axis-distance
# real -> q
# imag -> r
map = {
    "n": -1j,
    "ne": 1 - 1j,
    "se": 1,
    "s": 1j,
    "sw": -1 + 1j,
    "nw": -1,
}

# directions = ["se", "sw", "se", "sw", "sw"]
position = 0 + 0j
furthest = 0
new_distance = 0

for instr in directions:
    position += map[instr]
    new_distance = hex_manhattan(position)
    furthest = max(new_distance, furthest)

# Hex grid Manhattan distance half of cube-grid distance
print(int(new_distance // 2))
print(int(furthest // 2))
