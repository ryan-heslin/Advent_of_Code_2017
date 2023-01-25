from operator import attrgetter


def parse(lines):
    result = {}
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char != " ":
                result[complex(i, j)] = char
    return result


def neighbors(point):
    return {
        complex(point.real - 1, point.imag): -1 + 0j,
        complex(point.real + 1, point.imag): 1 + 0j,
        complex(point.real, point.imag - 1): 0 - 1j,
        complex(point.real, point.imag + 1): 0 + 1j,
    }


with open("inputs/day19.txt") as f:
    raw_input = f.read().splitlines()

grid = parse(raw_input)
position = min(grid.keys(), key=attrgetter("imag"))
direction = 0 + 1j
found = ""
traversed = 0
char = "-"

while char:
    last = position
    position += direction
    char = grid.get(position, "")
    traversed += 1
    if char.isalpha():
        found += char
    elif char == "+":
        this_neighbors = neighbors(position)
        for dest, dir in this_neighbors.items():
            if grid.get(dest) and dest != last:
                direction = dir
                break

print(found)
print(traversed)
