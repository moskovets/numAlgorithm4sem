"""
интерполяция функции на таблице значений с помощью полинома Ньютона
(с учетом экстраполяции)
"""

from math import sin, pi, factorial, cos
def f(x):
   return sin(x)
def df(x, n):
    if n % 4 == 0:
        return sin(x)
    elif n % 4 == 1:
        return cos(x)
    elif n % 4 == 2:
        return -sin(x)
    elif n % 4 == 3:
        return -cos(x)

def generate_table(start, end, step):
    table = []
    table.append([])
    table.append([])   
    for x in range(start, end + step, step):
        table[0].append(x)
        table[1].append(f(x))
    return table

def getCoefPolynomByConfiguration(conf, n):
    newconf = []
    for i in range(0, len(conf[0]) - n):
        #print(conf[1][i+1], conf[1][i])
        tmp = (conf[1][i+1] - conf[1][i]) / (conf[0][i+n] - conf[0][i] )
        newconf.append(tmp)
    return newconf

def interp(x, n, table):
    def binpoisk(x):
        a = 0
        b = len(table[0])
        while(b - a > 1):       
            m = int((a + b) / 2)
            #print(a, b, m, table[0][m])
            if table[0][m] > x:
                b = m
            elif table[0][m] == x:
                return m
            else:
                a = m
            #print("end\n")
        return a
    def findconf():
        conf = []
        conf.append([])
        conf.append([])
        #print(x)
        mid = binpoisk(x)
        #print("mid:", mid)
        left = max(0, mid - int(n/2))
        right = min(len(table[0]) - 1, left + n)
        left = max(0, right - n)
        for i in range(left, right + 1):
            conf[0].append(table[0][i])
            conf[1].append(table[1][i])
        return conf
    
    conf = findconf()
    #print("conf: ", conf)

    y = conf[1][0]
    for i in range(1, n + 1):
        coef = getCoefPolynomByConfiguration(conf, i)
        #print(coef)
        tmp = 1
        #print(conf)
        for j in range(0, i):
            #print(type(x))
            #print(type(conf[0][j]))
            t = x - conf[0][j]
            tmp *= t
        y += tmp * coef[0]
        j = 0
        for i in coef:
            conf[1][j] = i
            j += 1

    tmp *= x - conf[0][n]
    #print(tmp)

    eps = abs(tmp) / factorial(n + 1)
    #print(conf[0])
    df_conf = [abs(df(conf[0][i], n+1)) for i in range(0, len(conf[0]))]
    #print(df_conf)
    maxd = max(df_conf)
    eps *= maxd

    return y, eps

n = int(input("Введите степень полинома для интерполяции: "))
x = float(input("x = "))

table = generate_table(-5, 5, 1)
#for i in table:
#    print(i)

y, eps = interp(x, n, table)

print("Результат ", y)
print("Правильный ответ ", f(x))
print("\nПогрешность ", eps)
print("Абсолютная погрешность ", abs(y - f(x)))
