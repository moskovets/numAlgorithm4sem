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
    x = start
    while(x < end + step):
        #print(x)
        table[0].append(x)
        table[1].append(f(x))
        x += step
    return table

def get_table(filename):
    infile = open(filename, 'r')
    data = []
    data.append([])
    data.append([])   
    for line in infile:
        if line:
            a, b = map(float, line.split())
            data[0].append(a)
            data[1].append(b)
    infile.close()
    return data  

def getCoefPolynomByConfiguration(conf, n):
    newconf = []
    for i in range(0, len(conf[0]) - n):
        #print(conf[1][i+1], conf[1][i])
        tmp = (conf[1][i+1] - conf[1][i]) / (conf[0][i+n] - conf[0][i] )
        newconf.append(tmp)
    return newconf

def some_combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def GetCombineMult(arr, m):
	import itertools as it
	res = 0
#	pair = it.combinations(arr, m) # стандартная функция поиска всех нужных сочетаний
	pair = some_combinations(arr, m)
	for i in pair:
		flag = False
		tmp = 1
		for j in i:
			tmp *= j
		res += tmp
	return res

def deverative(x, n, table):
    def binpoisk(x):
        a = 0
        b = len(table[0])
        while(b - a > 1):       
            m = int((a + b) / 2)
            if table[0][m] > x:
                b = m
            elif table[0][m] == x:
                return m
            else:
                a = m
        return a

    def findconf():
        conf = []
        conf.append([])
        conf.append([])
        mid = binpoisk(x)
        left = max(0, mid - int(n/2))
        right = min(len(table[0]) - 1, left + n)
        left = max(0, right - n)
        for i in range(left, right + 1):
            conf[0].append(table[0][i])
            conf[1].append(table[1][i])
        return conf
    
    conf = findconf()

    y = 0

    for i in range(1, n + 1):
        coef = getCoefPolynomByConfiguration(conf, i)
        arr = []
        for j in range(0, i):
            t = x - conf[0][j]
            arr.append(t)
        tmp = GetCombineMult(arr, i - 1)

        y += tmp * coef[0]
        j = 0
        for i in coef:
            conf[1][j] = i
            j += 1

    return y

n = int(input("Введите количество узлов: "))
if n <= 0:
	print("error")
else:	
	x = float(input("x = "))

	table = generate_table(0, 5, 0.5)
	#table = get_table("der_table.txt") # если таблицу нужно из файла загрузить

	y = deverative(x, n - 1, table)

	print("Результат              ", y)
	print("Правильный ответ       ", f(x)) # актуально только для экспоненты
	print("Абсолютная погрешность ", abs(y - f(x)))
