import re
from string import ascii_lowercase


class Dancers(dict):
    def __init__(self, length):
        self.length = length
        index = range(0, length)
        if length < 27:
            names = ascii_lowercase
        else:
            names = index
        self.mapping = dict(zip(names, index))

    def __repr__(self):
        return str(self.mapping)

    def s(self, shift):
        self.mapping = {k: (v + shift) % self.length for k, v in self.mapping.items()}

    def p(self, name1, name2):
        self.mapping[name1], self.mapping[name2] = (
            self.mapping[name2],
            self.mapping[name1],
        )

    def x(self, pos1, pos2):
        self.mapping = {
            k: pos2 if v == pos1 else pos1 if v == pos2 else v
            for k, v in self.mapping.items()
        }


def parse_dance(instruction, instance="Order"):
    instruction = re.sub(r"\/", ",", instruction)
    match = r"([a-z])([^,]+)(,)?(.*)?"
    replace = r"\1(\2\3\4)"
    out = f"{instance}.{re.sub(match, replace, instruction)}"
    return re.sub(r"((?<=\(|,)[a-z](?=\)|,))", "'\\1'", out)


with open("inputs/day16.txt") as file:
    raw = file.read().split(",")

instance = "Order"
Order = Dancers(length=16)
parsed = tuple(map(parse_dance, raw))

for instruction in parsed:
    eval(instruction)

part1 = "".join(sorted(Order.mapping.keys(), key=lambda x: Order.mapping[x]))
print(part1)

Order = Dancers(length=16)
init = "".join(Order.mapping.keys())

iteration = 0
seen = {0: init}
while True:
    for instruction in parsed:
        exec(instruction)
    iteration += 1
    this = "".join(sorted(Order.mapping.keys(), key=lambda x: Order.mapping[x]))
    seen[iteration] = this
    if this == init:
        break

stop = 1000000000
leftover = stop % iteration
part2 = seen[leftover]
print(part2)
