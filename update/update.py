import ToUpdate as toUpdate
from pprint import pprint

levels = toUpdate.levels
for i in levels:
    for i2 in i[2]:
        i2[5].append(0)
pprint(levels)