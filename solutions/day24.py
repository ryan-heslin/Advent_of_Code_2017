with open("inputs/day24.txt") as file:
    raw = file.read().splitlines()


class Component:
    def __init__(self, inpt):
        self.lhs, self.rhs = [int(x) for x in inpt.split("/")]
        self.weight = self.lhs + self.rhs
        self.ports = {self.lhs, self.rhs}

    def __repr__(self):
        return f"{self.lhs}-+-{self.rhs}"

    def __eq__(self, other):
        return (
            isinstance(other, Component)
            and len(self.ports.intersection(other.ports)) > 0
        )

    def __ne__(self, other):
        return self.lhs != other.lhs or self.rhs != other.rhs

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def reverse(self):
        tmp = self.rhs
        self.rhs = self.lhs
        self.lhs = tmp
        return self


class Span:
    def __init__(self, component):
        if component.rhs == 0:
            self.end = component.reverse()
        elif component.lhs == 0:
            self.end = component
        else:
            raise ValueError
        self.weight = self.end.weight

    def extend(self, new):
        if new.lhs == self.end.rhs:
            self.end = new
        elif new.rhs == self.end.rhs:
            self.end = new.reverse()
        else:
            raise ValueError
        self.weight = self.weight + self.end.weight

    def __repr__(self):
        return f"{self.end.__repr__()} (weight {self.weight})"


def build_outer(components):
    found = []

    # Inner recursive function
    def build(end, components, weight, length):
        # pdb.set_trace()
        for i, component in enumerate(components):
            if end.rhs in component.ports:
                if end.rhs == component.lhs:
                    next_c = component
                else:
                    next_c = component.reverse()
                build(
                    next_c,
                    list(set(components) - {components[i]}),
                    weight + next_c.weight,
                    length + 1,
                )
            else:
                pass
        found.append({"weight": weight, "length": length})

    init = Component("0/0")
    build(init, components, weight=init.weight, length=0)
    maxes = tuple(max(found, key=lambda x: x[attr]) for attr in ("weight", "length"))
    part2 = max(
        bridge["weight"] for bridge in found if bridge["length"] == maxes[1]["length"]
    )
    return (maxes[0]["weight"], part2)


parsed = list(map(Component, raw))
result = tuple(build_outer(parsed))
print(result[0])
print(result[1])
