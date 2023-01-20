import os
import re


with open("inputs/day7.txt") as file:
    orig = [line.rstrip("\n") for line in file.readlines()]
file.close()


depends = dict(
    [
        [
            re.search("^[a-z]+", line).group(),
            re.search("(?<=>\s).*", line).group().split(", "),
        ]
        for line in filter(lambda x: ">" in x, orig)
    ]
)


def find_bottom(di):

    comp = {*di.keys()}
    di = dict(filter(lambda x: any([el in comp for el in x[1]]), di.items()))

    if len(di.keys()) == 1:

        return di.keys()
    else:
        return find_bottom(di)


ans1 = find_bottom(depends)

print(f"Part 1: {''.join(ans1)}")

weights = {
    re.search("^[a-z]+", line).group(): int(re.search("\\d+", line).group())
    for line in orig
}


def expand_values(key, di):
    if di[key] is None:
        return weights[key]
    else:
        return [expand_values(prog, di) for prog in di[key]]


def traverse_weights(key, di):
    if di[key] is None:
        return total_weights[key]
    else:
        l = list(map(lambda k: total_weights[k], di[key]))
        if not all(x == l[0] for x in l):
            print(f"{k}")
            for prog in di[key]:
                print(f"{prog}: {total_weights[prog]}")
        return [expand_values(prog, di) for prog in di[key]]


depends2 = [None] * len(orig)
for i, line in enumerate(orig):
    if ">" in line:
        depends2[i] = [
            re.search("^[a-z]+", line).group(),
            re.search("(?<=>\s).*", line).group().split(", "),
        ]
    else:
        depends2[i] = [re.search("^[a-z]+", line).group(), None]
depends2 = dict(depends2)


# From https://stackoverflow.com/questions/12472338/flattening-a-list-recursively
flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]
total_weights = {
    k: sum(flatten([expand_values(k, depends2)])) for k, v in depends2.items()
}

for k, v in {k: v for k, v in total_weights.items() if v}.items():
    if depends2[k]:
        disc = list(map(lambda x: total_weights[x], depends2[k]))
        if disc and not all(x == disc[0] for x in disc):
            print(disc)
for k in depends2.keys():
    traverse_weights(k, depends2)


print(f"Part 2: {ans2}")
