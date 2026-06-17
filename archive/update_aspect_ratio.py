import re

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Change the grid container to have max-width and center it
old_grid = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 40px;">'
new_grid = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 40px auto 0; max-width: 600px;">'

text = text.replace(old_grid, new_grid)

# Change height: 200px; to aspect-ratio: 4/3;
# Ensure we only replace within the buttons
text = text.replace('height: 200px;', 'aspect-ratio: 4/3;')

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("script.js updated to 4:3 aspect ratio and centered.")
