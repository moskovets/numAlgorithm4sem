"""
Часть 1. Численной дифференцирование
1. односторонние разности
2. центральная разность
3. повышенная точность в граничных точках
4. фурмулы Рунге
5. Выравнивающие переменные (для экспоненты)
Задается х, для которого необходимо найти производную
"""

import numpy as np
import pandas as pd

from math import exp, log

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
	a = []
	for i in range(0, n - 1):
		dx = table[i+1][0] - table[i][0]
		if dx == 0:
			a.append(None)
		else:
			a.append((table[i+1][1] - table[i][1]) / dx)
	a.append(None)
	return np.array(a)

#2. центральная разность
def diff_central(table):
	n = table.shape[0]
	a = [None]
	for i in range(1, n - 1):
		dx = table[i+1][0] - table[i-1][0]
		if dx == 0:
			a.append(None)
		else:
			a.append((table[i+1][1] - table[i-1][1]) / dx) 
	a.append(None)
	## нужно ли добавлять производные на границах? 
	return np.array(a)

#3. повышенная точность в граничных точках
def border_derevative(table):
	n = table.shape[0]
	a = [None for i in range(0, n)]

	dx0 = table[2][0] - table[0][0]
	dxn = table[n-1][0] - table[n-3][0]


	if dx0 != 0:
		a[0] = (-3 * table[0][1] + 4 * table[1][1] - table[2][1]) / dx0

	if dxn != 0:
		a[n-1] = (3 * table[n-1][1] - 4 * table[n-2][1] + table[n-3][1]) / dxn

	return np.array(a)

#5. Выравнивающие переменные (для экспоненты)
def ksi(x):
	return x
def eta(y):
	return log(y)
def leveling_variables(table):
	new_table = np.array([[ksi(i[0]), eta(i[1])] for i in table])

	a = diff_one_side(new_table) #eta'ksi
	a[-1] = 0
	#print(a)
	#print(table[:,1])
	a = a * table[:,1]
	a[-1] = None
	return a

table = generate_table(-5, 5, 1)

one_side = diff_one_side(table)
central = diff_central(table)
border = border_derevative(table)

leveling = leveling_variables(table)

res = np.column_stack((table, one_side, central, border, leveling))

s = pd.DataFrame(res, columns=['x', 'f(x)', 'одностор.разности', 'центр.разности', 'на границах', 'выр.перем.'])
print(s)
