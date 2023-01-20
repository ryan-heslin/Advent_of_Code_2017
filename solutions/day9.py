import functools as ft
import re

with open("inputs/day9.txt") as file:
    raw_input = file.read()

patterns = (r"!.", r"<[^>]*>", r"[^\}\{]")

cleaned = ft.reduce(lambda line, pat: re.sub(pat, "", line), patterns, raw_input)

score = depth = 0
for char in cleaned:
    if char == "{":
        depth += 1
        score += depth
    else:
        depth -= 1

print(score)

cleaned_part2 = re.sub("!.", "", raw_input)

part2 = len(cleaned_part2) - len(re.sub("<[^>]*>", "<>", cleaned_part2))
print(part2)
