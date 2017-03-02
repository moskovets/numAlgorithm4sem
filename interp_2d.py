"""
многомерная интерполяции на примере нахождения значений функции 2-х переменных
"""

from math import sin, pi, factorial, cos, exp, log
eps_const = 0.00001
eps_otn = 0.0001
def f_0(x, y):
	return x*x + y*y

#[[x, [y,y,y,y], [z,z,z,z]], ]
def generate_table(f, parx, pary):
    startx, endx, stepx = parx
    if(pary == ()):
    	starty = startx; endy = endx; stepy = stepx
    else:
    	starty, endy, stepy = pary

    table = []
    x = startx
    j = 0
    while(x < endx + stepx):
        y = starty
        table.append([x, [], []])
        while(y < endy + stepy):
	        #print(x)
	        table[j][1].append(y)
	        table[j][2].append(f(x, y))
	        y += stepy
        x += stepx
        j += 1
    return table

# поиск конфигурации по х
def find_list_x(table, x, n):
    a = 0
    b = len(table)
    while(b - a > 1):       
        m = int((a + b) / 2)
        #print(a, b, m, table[0][m])
        if table[m][0] > x:
            b = m
        elif table[m][0] == x:
            return m
        else:
            a = m
    mid = a

    res = []
    left = max(0, mid - int((n + 1)/2))
    right = min(len(table) - 1, left + n)
    left = max(0, right - n)
    for i in range(left, right + 1):
        res.append(i) 
    return res

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
        #print(table[0])
        #print(left, right)
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


n = int(input("Введите степень полинома для интерполяции x: "))
x = float(input("x = "))
m = int(input("Введите степень полинома для интерполяции y: "))
y = float(input("y = "))

table = generate_table(f_0, (0, 5, 1), ())
print(table[0][1:3])
x_l = find_list_x(table, x, n)

tablex = []
tablex.append([])
tablex.append([])
for i in x_l:
	tablex[0].append(table[i][0])
	tmp = interp(y, m, table[i][1:3])
	tablex[1].append(tmp)

#print(tablex)
z = interp(x, n, tablex)
print("Результат ", z)
print("Правильный ответ ", f_0(x, y))

