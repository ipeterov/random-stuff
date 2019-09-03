import matplotlib.pyplot as plt
import pickle

whole = []
days = pickle.load(open('function_days', 'rb'))
for day in days:
    whole.extend(day)

plt.plot(whole)
plt.show()