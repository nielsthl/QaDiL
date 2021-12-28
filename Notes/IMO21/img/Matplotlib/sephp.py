#import numpy as np
import matplotlib
#matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt

plt.plot([1.35, 1.42, 1.45, 1.52], [35, 50, 40, 45], 'ro')

plt.plot([1.68, 1.70, 1.73, 1.73], [65, 70, 60, 80], 'bo')

plt.axis([1.3, 1.8, 30, 90])

plt.xlabel("height (m)")

plt.ylabel("weight (kg)")

plt.show()
