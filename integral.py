"""
Данная программа считает определенный интеграл методом трапеций для функции, заданной неявно
Значение функции находится с помощью меода половинного деления
"""
from math import sin, cos, exp

def half_div_method(a, b, eps, x):
    def f(y):
        c1 = exp(x**3)
        c2 = -2*(x**3) + 2
        c3 = c2 + x**6
        return c1 - exp(y) * (c3 + c2 * y + y*y)
    x1 = a
    x2 = b
    eps = (b - a) * eps
    while abs(x2 - x1) > eps:
        mid = (x1 + x2) / 2
        fm = f(mid)
        if(fm == 0):
            return mid
        if(fm * f(x1) < 0):
            x2 = mid
        else:
            x1 = mid 
    if abs(f(x1)) > abs(f(x2)):
        return x2
    return x1

def f(x, eps):
    return half_div_method(-10, 10, eps, x)

def trap(n, eps):
    h = (b - a) / n
    x = a
    s = 0
    for i in range(n):
        s += f(x, eps) + f(x + h, eps)
        x += h
    I = s * h / 2
    return I

#a, b = map(float, input("Введите a и b через пробел: ").split())
#eps = float(input("Введите точность вычислений eps = "))
a = 0
b = 2
eps_otn = 0.0001
eps = (b - a) * eps_otn

n = 1
I1 = trap(n, eps_otn)
I2 = trap(n * 2, eps_otn)
n *= 2
while abs(I2 - I1)  > eps:
    I1, I2 = I2, I1
    n *= 2
    I2 = trap(n, eps_otn)

print("Значение определенного интеграла", '{:9.5f}'.format(I2))
