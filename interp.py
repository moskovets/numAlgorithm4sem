from math import sin, pi
def f(x):
   return sin(pi/6 * x)

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

n = int(input("Введите степень полинома для интерполяции: "))
x = float(input("x = "))

table = generate_table(-3, 3, 1)
#for i in table:
#    print(i)

y = interp(x, n, table)
print(y)
print(f(x))