#!/usr/bin/env python
# coding: utf-8

import sqlite3
import time
import sys


conn = sqlite3.connect('/home/ipeterov/weight_monit/weight_data.sqlite')
cursor = conn.cursor()

if len(sys.argv) > 1:
    weight = float(sys.argv[1])
else:
    weight = float(raw_input('Измеренный вес: '))

log_time = int(time.time())

query = 'INSERT INTO weights VALUES ({weight}, {log_time})'.format(weight=weight, log_time=log_time)
cursor.execute(query)

conn.commit()
conn.close()
