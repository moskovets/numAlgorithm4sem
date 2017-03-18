"""
наилучшее среднеквадратичное приближениеи 
"""
from math import sin, pi, factorial, cos, exp, log

from collections import namedtuple
Table = namedtuple('Table', ['x','y', 'w']) # w = вес функции

eps_const = 0.00001
eps_otn = 0.0001
def fi(x, k):
    return x ** k

def get_table(filename):
    infile = open(filename, 'r')
    data = []
    for line in infile:
        a, b, c = map(float, line.split())
        data.append(Table(a, b, c))
    print(data)
    infile.close()
    return data


def print_result(table, A, n):
    import numpy as np
    import matplotlib.pyplot as plt
    dx = 10
    if len(table) > 1:
        dx = (table[1].x - table[0].x)

    # построение аппроксимирующей функции    
    x = np.linspace(table[0].x - dx, table[-1].x + dx, 100)
    y = []
    for i in x:
        tmp = 0;
        for j in range(0, n + 1):
            tmp += fi(i, j) * A[j]
        y.append(tmp)

    plt.plot(x, y)

    #построение исходной таблицы
    x1 = [a.x for a in table]
    y1 = [a.y for a in table]


    plt.plot(x1, y1, 'kD', color = 'green', label = '$исходная таблица$')
    plt.grid(True)
    plt.legend(loc = 'best')
    plt.axis([table[0].x - dx, table[-1].x + dx, min(min(y), min(y1)), max(max(y), max(y1))])

    plt.show()
    return 

table = get_table("table.txt")

n = int(input("Введите степень полинома n = "))

A = [1 for i in range(0, n+1)]

print_result(table, A, n)
