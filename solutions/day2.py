with open("inputs/day2.txt") as f:
    raw_input = f.read().splitlines()


processed = [[int(y) for y in x.split()] for x in raw_input]
part1 = sum(max(x) - min(x) for x in processed)
print(part1)

n_nums = len(processed[0])
part2 = 0
for row in processed:
    sorting = sorted(row, key=lambda x: -x)
    done = False
    for dividend in sorting:
        if done:
            break
        for divisor in filter(lambda x: x < dividend, sorting):
            result = dividend / divisor
            if result == dividend // divisor:
                part2 += result
                done = True
                break

print(part2)
