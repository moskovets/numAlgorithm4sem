"""
Часть 1. Численной дифференцирование
1. односторонние разности
2. центральная разность
3. повышенная точность в граничных точках
4. фурмулы Рунге
5. Выравнивающие параметры (для экспоненты)
Задается х, для которого необходимо найти производную
"""

import numpy as np
import pandas as pd

from math import *

def f(x):
   return exp(x)

def generate_table(start, end, step):
    table = []
    for x in range(start, end + step, step):
        table.append([x, f(x)])
    return np.array(table)

#1. односторонние разности
def diff_one_side(table):
	n = table.shape[0]
	print(n)
	a = []
	for i in range(0, n - 1):
		dx = table[i+1][0] - table[i][0]
		if dx == 0:
			a.append(NaN)
		else:
			a.append((table[i+1][1] - table[i][1]) / dx)
	a.append(None)
	return np.array(a)


table = generate_table(-5, 5, 1)

one_side = diff_one_side(table)

res = np.column_stack((table, one_side))

s = pd.DataFrame(res, columns=['x', 'f(x)', 'одностор.разности'])
print(s)
