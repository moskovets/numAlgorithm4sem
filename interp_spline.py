"""
интерполяция сплайнами 
"""
from math import sin, pi, factorial, cos, exp, log

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
Progon_coef = namedtuple('Progon_coef', ['ksi', 'eta'])
interp_coef = namedtuple('interp_coef', ['a', 'b', 'c', 'd'])
coef_slau = namedtuple('coef_slau', ['A', 'B', 'D', 'F'])
temporary_coef = namedtuple('temporary_coef', ['h', 'dyh'])

eps_const = 0.00001
eps_otn = 0.0001
def f_0(x):
   return sin(x)

#[[x,x, x, x], [y,y,y,y]]
def generate_table(f, start, end, step):
    table = []
    for x in range(start, end + step, step):
        table.append(Point(x, f(x)))
    return table

def Get_temporary_coef(table):
	coef = []
	coef.append(temporary_coef(0, 0))
	
	N = len(table)
	
	for i in range(1, N + 1):
		h_i = table[i].x - table[i-1].x
		dyh_i = (table[i].y - table[i-1].y) / h_i

		coef.append(temporary_coef(h_i, dyh_i))

	return coef

def Get_coef_slau(tmp_coef):
	coef = []
	coef.append(coef_slau(0, 0, 0, 0))
	coef.append(coef_slau(0, 0, 0, 0))
	
	N = len(tmp_coef)
	
	for i in range(2, N + 1):

		a = tmp_coef[i-1].h
		b = -2 * (tmp_coef[i-1].h + tmp_coef[i].h)
		d = tmp_coef[i].h
		f = -3 * (tmp_coef[i].tmp - tmp_coef[i-1].tmp)
		coef.append(coef_slau(a, b, d, f))

	return coef

def Get_progon_coef(slau):
	progon = []
	progon.append(Progon_coef(0, 0)) #0
	progon.append(Progon_coef(0, 0)) #1

	N = len(slau)

	eta = 0
	ksi = 0
	progon.append(Progon_coef(eta, ksi)) #2

	for i in range(2, N):
		znam = slau[i].B - slau[i].A * ksi 

		eta = (slau[i].A * ets + slau[i].F) / znam
		ksi = slau[i].D / znam

		progon.append(Progon_coef(eta, ksi)) #i + 1

	return progon
def Get_interp_coef(c, tmp_coef, table):
	res = []

	return res
	

def interp(table):
	tmp_coef = Get_temporary_coef(table)

	slau = Get_coef_slau(tmp_coef)

	progon = Get_progon_coef(slau)

	N = len(table)

	c = []
	c.append = (-slau[N].F - slau[N].A * progon[N].eta) / (-slau[N].B + slau[N].A * progon[N].ksi)
	for i in range(N - 1, 0):
		c.append(progon[i].ksi * c[-1] + progon[i].eta)
	c.append(0)
	c = c[::-1]

	res = Get_interp_coef(c, tmp_coef, table)

	return res

x = float(input("x = "))

table = generate_table(f_0, 0, 3, 0.5)

y = interp(x, table)

print("Результат ", y)
print("Правильный ответ ", f_0(x))

