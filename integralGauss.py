"""
данная программа находит верхний передел интегрирования по заданной функции и значению интеграла
интеграл вычисляется методом Гаусса с помощью составление квадратурной формулы Гаусса 
по корням полинома Лежандра заданной степени
"""
from math import cos, pi, exp, sqrt
import numpy as np

eps = 0.0001
def f(t):
    return exp(-t * t / 2)

def get_polinom_Legendre(n, x):
    p = []
    p.append(1)
    p.append(x)
    i = 2
    while i <= n:
        tmp = (2 * i - 1) * x * p[i - 1] - (i - 1) * p[i - 2]
        tmp /= i
        p.append(tmp)
        i += 1
    return p

def get_deveration_polinom_Legendre(n, p, x):
    res = n / (1 - x * x) * (p[n - 1] - x * p[n])
    return res

# можно оптимизировать поиском первой половины корней
def get_roots_Legendre(n):

	# если i брать в ест. порядке, то получится от большего к меньшему
    x = [cos(pi * (4 * i - 1) / (4 * n + 2)) for i in range(n, 0, -1)]     
#    print(x)
    px = []
    dpx = []
    for i in range(0, n):
        p = []
        dp = []
        while True:
            p  = get_polinom_Legendre(n, x[i])
            dp = get_deveration_polinom_Legendre(n, p, x[i])
            dx = p[n] / dp
            x[i] -= dx
            if abs(dx) < eps:
                break
        px.append(p)
        dpx.append(dp)
    return x, px, dpx

def get_coef_Gauss_formula(x, dp, n):
    def getA(i):
        return 2 / (1 - x[i] * x[i]) / (dp[i] * dp[i]) 


    a = [getA(i) for i in range(0, n)]
    return a
# работает хуже чем формула
def get_coef_Gauss(x, n):
    z = []
    for i in range(0, n):
        if i % 2 == 0:
            z.append(2 / (i + 1))
        else:
            z.append(0)

    matr = []
    matr.append([1 for i in range(0, n)])
    for i in range(1, n):
        matr.append([])
        for j in range (0, n):
            matr[i].append(matr[i-1][j] * x[j])
    res = np.linalg.solve(matr, z) ########
    return res
def F(x, alpha, t, weights):
	res = 0
	n = len(t)
	for i in range(0, n):
		res += weights[i] * f(x / 2 * t[i]) ## modife if lower limit is not 0
	res *= x / 2
	return res - alpha


#a, b - значения для поиска (а = 0) 
def find_limit_of_integration(a, b, alpha, t, weights):
	print(a, F(a, alpha, t, weights))
	print(alpha)
	if(F(a, alpha, t, weights) > 0):
		a, b = b, a
	if(F(a, alpha, t, weights) > 0):
		print("Увеличить диапазон поиска!")
		return
	tmp = 0
	j = 0
#	while True:
	while j < 10:
		#j += 1
		tmp = (a + b) / 2
		Ftmp = F(tmp, alpha, t, weights)
		print(tmp, Ftmp)

		if abs((b - tmp) / b) < eps:
			break
		if Ftmp < 0:
			a = tmp
		else:
			b = tmp
	return tmp

n = int(input("n = "))
alpha = float(input("a = "))
alpha *= sqrt(2 * pi)
x, px, dpx = get_roots_Legendre(n)
print("Корни полинома Лежандра:")
print(x)

print("Весовые коэф. по формуле:")
a = get_coef_Gauss_formula(x, dpx, n)
print(a)

print("Коэф. по решению системы:")
b = get_coef_Gauss(x, n)
print(b)


res = find_limit_of_integration(0, 5, alpha, x, b)
print("x = ", res)

import matplotlib.pyplot as plt
tx = np.linspace(0, 20, 100)
y = [F(i, alpha, x, b) for i in tx]
plt.plot(tx, y)
plt.show()