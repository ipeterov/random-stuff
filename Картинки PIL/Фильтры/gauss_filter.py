import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

mu = 0 # mean of distribution
sigma = 1 # standard deviation of distribution


graph = []
a = []
for i in range(-100, 100):
    i /= 10
    graph.append(mlab.normpdf(i, mu, sigma))
    a.append(i)

plt.plot(a, graph)
plt.show()
