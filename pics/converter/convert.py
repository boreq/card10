import sys
from PIL import Image


im = Image.open(sys.argv[1]) # Can be many different formats.
pix = im.load()


width, height = im.size

print('image = [')

for y in range(height):
    print('    [')
    a = []
    for x in range(width):
        v = pix[x, y] 
        if v[3] < 0.5:
            a.append('None')
        else:
            a.append(str([v[0], v[1], v[2]]))
    print('        ', end='')
    print(', '.join(a))
    if y == height - 1:
        print('    ]')
    else:
        print('    ],')

print(']')
