step_len = 354
length = 2018


class Circle:
    def __init__(self, step):
        self.current_len = 1
        self.step = step
        self.sequence = [0]

    def __repr__(self):
        return str(self.sequence)

    def make_step(self, max_len):
        current_i = 0
        for i in range(self.current_len, max_len):
            next_i = ((current_i + self.step) % i) + 1
            self.sequence.insert(next_i, i)
            current_i = next_i
        self.current_len = max_len

    def after_max(self):
        return self.sequence[self.sequence.index(max(self.sequence)) + 1]


Part1 = Circle(step_len)
Part1.make_step(length)
part1 = Part1.after_max()
print(part1)

current_i, after_zero = 0, 0
for i in range(1, 50000000):
    current_i = ((current_i + step_len) % i) + 1

print(current_i)
