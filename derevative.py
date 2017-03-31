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


table = generate_table(-5, 5, 1)

s = pd.DataFrame(table, columns=['x', 'f(x)'])

print(s)
