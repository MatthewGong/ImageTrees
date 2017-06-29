import numpy as np
import random

#tempColor = np.random.randint(0,255, 50)

tempColor = range(0, 255, 6)

random.shuffle(tempColor)

print tempColor

string = ""

for color in tempColor:
	string += str(color) + ","