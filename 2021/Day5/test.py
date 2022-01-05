import re



match = re.match(r"(\d+),(\d+)\s->\s(\d+),(\d+)", "5,5 -> 8,2")

tuple(map(int, match.group(1,2)))