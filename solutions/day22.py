def parse(lines):
    result = {}
    for j, line in enumerate(reversed(lines)):
        for i, char in enumerate(line):
            if char == "#":
                result[(complex(i, j))] = 1

    return result, complex(len(lines) // 2, len(lines[0]) // 2)


def simulate(grid, iterations, start):
    position = start
    direction = 0 + 1j
    infections = 0

    for _ in range(iterations):
        if position in grid.keys():
            direction = complex(direction.imag, -direction.real)
            grid.pop(position)
        else:
            infections += 1
            direction = complex(-direction.imag, direction.real)
            grid[position] = 1
        position += direction

    return infections


def simulate_part2(grid, iterations, start):
    position = start
    direction = 0 + 1j
    infections = 0

    # 2 -> weakened
    # 1 -> infected
    # 0 -> flagged
    # clean -> not stored

    for _ in range(iterations):
        if position not in grid.keys():  # Clean
            direction = complex(-direction.imag, direction.real)
            grid[position] = 2
        elif grid[position] == 2:  # weakened
            infections += 1
            grid[position] = 1
        elif grid[position] == 1:  # infected
            grid[position] = 0
            direction = complex(direction.imag, -direction.real)
        else:  # Flagged
            grid.pop(position)
            direction = -direction
        position += direction

    return infections


with open("inputs/day22.txt") as f:
    raw_input = f.read().splitlines()

grid, start = parse(raw_input)
part1_i = 10000
part2_i = 10000000
part1 = simulate(grid.copy(), part1_i, start)
print(part1)

part2 = simulate_part2(grid, part2_i, start)
print(part2)
