import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

# Generate data:
x = y = np.linspace(-100, 100, 10)
z = x**2 + y**2

# Set up a regular grid of interpolation points
xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
xi, yi = np.meshgrid(xi, yi)

# Interpolate
rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
zi = rbf(xi, yi)

plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower', extent=[x.min(), x.max(), y.min(), y.max()])
#plt.scatter(x, y, c=z)
plt.colorbar()
plt.show()