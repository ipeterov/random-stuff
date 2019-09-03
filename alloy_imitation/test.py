import numpy as np
import matplotlib.pyplot as plt

a = np.fromfunction(lambda de, t: np.exp(-de/t), (200, 1000))

plt.imshow(a, cmap='gray')
plt.show()
