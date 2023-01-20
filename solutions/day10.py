def knot_hash(lengths):
    current = skip_size = 0
    numbers = list(range(5))
    n = len(numbers)

    for length in lengths:
        if length <= n:
            end = current + length
            overlap_end = end % n
            if end == overlap_end:
                numbers[current : (end + 1)] = reversed(numbers[current : (end + 1)])
            else:
                reversal = numbers[current:] + numbers[: (overlap_end + 1)]

            numbers[current]
            current += skip_size + length
            current %= n
            skip_size += 1
    return numbers


with open("inputs/day10.txt") as f:
    raw_input = f.read()

lengths = [int(x) for x in raw_input.split(",")]
lengths = [3, 4, 1, 5]
hashed = knot_hash(lengths)
part1 = hashed[0] * hashed[1]
print(part1)
