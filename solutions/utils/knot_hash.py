from functools import reduce
from operator import xor


def knot_hash(lengths, n, rounds=1):
    current = skip_size = 0
    numbers = list(range(n))

    for _ in range(rounds):

        for length in lengths:
            # Add length MINUS 1 to get stop index
            # e.g., length 1 selects element itself
            if length <= n:
                end = current + length - 1
                overlap_end = end % n
                if end < n:
                    numbers[current : (end + 1)] = reversed(
                        numbers[current : (end + 1)]
                    )
                else:
                    reversal = numbers[current:] + numbers[: (overlap_end + 1)]
                    numbers[: overlap_end + 1] = reversal[overlap_end::-1]
                    numbers[current:] = reversal[
                        : len(reversal) - (n - current + 1) : -1
                    ]

                current += skip_size + length
                current %= n
                skip_size += 1
    return numbers


def complete_hash(lengths, n=256, rounds=1):
    chunk_size = 16
    lengths = process_input(lengths)
    hashed = knot_hash(lengths, n, rounds=rounds)
    dense_hash = [
        reduce_xor(hashed[i : (i + chunk_size)]) for i in range(0, n, chunk_size)
    ]
    return finish_hash(dense_hash)


def reduce_xor(xs):
    return reduce(xor, xs)


def process_input(inp):
    return list(ord(x) for x in inp) + [17, 31, 73, 47, 23]


def finish_hash(numbers):
    return "".join(hex(x)[2:].zfill(2) for x in numbers)
