# coding: utf-8

import datetime
import sqlite3

import matplotlib.pyplot as plt

conn = sqlite3.connect('/home/ipeterov/weight_monit/weight_data.sqlite')
cursor = conn.cursor()

dates = []
weights = []
for row in cursor.execute('SELECT * FROM weights'):
    dates.append(datetime.datetime.fromtimestamp(row[1]))
    weights.append(row[0])

conn.close()

plt.plot_date(x=dates, y=weights, fmt="r-")
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()
