with open("other_disability_data.js", "r", encoding="utf-8") as f:
    lines = [f.readline() for _ in range(30)]
print("other_disability_data.js:")
print("".join(lines))

print("\n" + "="*40 + "\n")

with open("other_disability.js", "r", encoding="utf-8") as f:
    lines2 = [f.readline() for _ in range(30)]
print("other_disability.js:")
print("".join(lines2))
