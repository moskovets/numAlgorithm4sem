"""
интерполяция функции на таблице значений с помощью полинома Ньютона
(с учетом экстраполяции)
"""

from math import sin, pi, factorial, cos, exp

def f(x):
   return exp(x)

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

def GetCombineMult(arr, m):
	import itertools as it
	res = 0
	pair = it.combinations(arr, m)
	for i in pair:
		flag = False
		tmp = 1
		for j in i:
			print(j)
			tmp *= j
		res += tmp
	print(res)
	return res

def deverative(x, n, table):
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
    print("conf: ", conf)

    y = 0

    for i in range(1, n + 1):
        coef = getCoefPolynomByConfiguration(conf, i)
        #print(coef)
        arr = []
        #print(conf)
        for j in range(0, i):
            t = x - conf[0][j]
            arr.append(t)
        #print(arr)    
        tmp = GetCombineMult(arr, i - 1)

        #print("\n", coef[0])

        y += tmp * coef[0]
        j = 0
        for i in coef:
            conf[1][j] = i
            j += 1

    return y

n = int(input("Введите количество узлов: "))

x = float(input("x = "))

table = generate_table(0, 5, 1)

y = deverative(x, n - 1, table)

print("Результат              ", y)
print("Правильный ответ       ", f(x))
print("Абсолютная погрешность ", abs(y - f(x)))
