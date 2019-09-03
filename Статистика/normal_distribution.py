import random
import matplotlib.pyplot as plt

sample_len = 50
samples_count = 10000

data = [sum([random.choice((1,-1)) for _ in range(sample_len)]) for _ in range(samples_count)]
a = plt.hist(data, bins=50, histtype='bar')
#~ plt.plot(a)
plt.show()

