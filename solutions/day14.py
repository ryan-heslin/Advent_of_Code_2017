from collections import defaultdict
from collections import deque

import utils.knot_hash as kh


def hash2bits(hash):
    return "".join(mapping[x] for x in hash)


def create_rows(stem, rows=128):
    filled = set()
    for i in range(rows):
        hash = kh.complete_hash(stem + "-" + str(i), n=256, rounds=64)
        number = hash2bits(hash)
        filled.update((complex(j, i) for j, char in enumerate(number) if char == "1"))
    return filled


def flood_fill(coords):
    i = -1
    regions = defaultdict(lambda: deque([]))
    Q = deque([])

    while coords:
        if not Q:
            Q.appendleft(coords.pop())
            i += 1
        current = Q.popleft()
        coords.discard(current)
        regions[i].appendleft(current)
        current_neighbors = neighbors(current)

        for neighbor in current_neighbors:
            if neighbor in coords:
                Q.appendleft(neighbor)

    return len(regions.keys())


def neighbors(x):
    return (
        complex(x.real - 1, x.imag),
        complex(x.real + 1, x.imag),
        complex(x.real, x.imag - 1),
        complex(x.real, x.imag + 1),
    )


hex_digits = "0123456789abcdef"
values = (bin(int(x, 16))[2:].zfill(4) for x in hex_digits)
mapping = dict(zip(hex_digits, values))


raw_input = "oundnydw"
filled = create_rows(stem=raw_input)
part1 = len(filled)
print(part1)

part2 = flood_fill(filled)
print(part2)
