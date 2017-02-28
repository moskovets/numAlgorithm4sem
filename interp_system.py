"""
решение системы нелинейных уравнений
с помощью интерполяции
"""

from math import sin, pi, factorial, cos, exp, log
eps_const = 0.00001
eps_otn = 0.0001
def f1y(x, y):
	x3 = x**3
	return exp(x3-y) - x3 * (x3 - 2 * y - 2) - y * y - 2 * y - 2
def f2y(x, y):
	return x*x*exp(- y)  + y * exp(-y) - exp(x*x) * log(x*x + y)


def half_div_method(a, b, eps, x, f):
    x1 = a
    x2 = b
    eps = (b - a) * eps
    while True:
        mid = (x1 + x2) / 2
        if abs(x2 - x1) < eps * abs(mid) + eps_const:
        	break
        fm = f(x, mid)
        if(fm == 0):
            return mid
        if(fm * f(x, x1) < 0):
            x2 = mid
        else:
            x1 = mid 
    if abs(f(x, x1)) > abs(f(x, x2)):
        return x2
    return x1

def f1(x):
   return half_div_method(-1, 2, eps_otn, x, f1y)

def f2(x):
    return half_div_method(0.1, 2, eps_otn, x, f2y)


def generate_table(start, end, step, f):
    table = []
    table.append([])
    table.append([])   
    x = start
    while(x < end + step):
        #print(x)
        table[0].append(x)
        table[1].append(f(x))
        x += step
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
        left = max(0, mid - int((n + 1)/2))
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


    return y

def my_sort(table):
	for i in range(0, len(table[1])):
		for j in range(1, len(table[1])):
			if table[0][j] < table[0][j - 1]:
				table[0][j], table[0][j - 1] = table[0][j - 1], table[0][j]
				table[1][j], table[1][j - 1] = table[1][j - 1], table[1][j]
	return table





table1 = generate_table(0, 1, 0.1, f1)
#print("ok1")
table2 = generate_table(0, 1, 0.1, f2)
#print("ok2")
table3 = []
table3.append([])
table3.append([])  

for i in range(0, len(table1[1])):
    table3[1].append(table1[0][i])
    table3[0].append(table2[1][i] - table1[1][i])
#    print(table3[0][i], table3[1][i])

#print()
table3 = my_sort(table3)

#for i in range(0, len(table1[1])):
#    print(table3[0][i], table3[1][i])

x = 0
n = 4
x = interp(x, n, table3)

print("Результат x = ", x)
y1 = f1(x)
y2 = f2(x)
print("y = ", y1 + (y2 - y1) / 2)
