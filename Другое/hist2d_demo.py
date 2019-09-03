import matplotlib.pyplot as plt
import numpy as np
x = np.random.randn(1000)
y = np.random.randn(1000) + 5

print(list(x), list(y))
# normal distribution center at x=0 and y=5
plt.hist2d(x, y, bins=80)
plt.show()
