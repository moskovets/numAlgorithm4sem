"""
интерполяция сплайнами 
"""
from math import sin, pi, factorial, cos, exp, log

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
Progon_coef = namedtuple('Progon_coef', ['eta', 'ksi'])
interp_coef = namedtuple('interp_coef', ['a', 'b', 'c', 'd'])
coef_slau = namedtuple('coef_slau', ['A', 'B', 'D', 'F'])
temporary_coef = namedtuple('temporary_coef', ['h', 'dyh'])

eps_const = 0.00001
eps_otn = 0.0001
def f_1(x):
   return sin(4*x)
def f_2(x):
   return sin(x)
def f_0(x):
   return x * x

#[[x,x, x, x], [y,y,y,y]]
def generate_table(f, start, end, step):
	table = []
	x = start
	while x < end + step:
		table.append(Point(x, f(x)))
		x += step
	return table

def table_from_wiki():
	table = []
	table.append(Point(1, 1.0002))
	table.append(Point(2, 1.0341))
	table.append(Point(3, 0.6))
	table.append(Point(4, 0.40105))
	table.append(Point(5, 0.1))
	table.append(Point(6, 0.2397))
	return table
def table_from_wiki_2():
	table = []
	table.append(Point(1, 5))
	table.append(Point(2, 3))
	table.append(Point(3, 2.5))
	table.append(Point(4, 2))
	table.append(Point(5, 0))
	return table


def Get_temporary_coef(table):
	coef = []
	coef.append(temporary_coef(0, 0))
	
	N = len(table) - 1
	
	for i in range(1, N + 1):
		h_i = table[i].x - table[i-1].x
		dyh_i = (table[i].y - table[i-1].y) / h_i

		coef.append(temporary_coef(h_i, dyh_i))

	return coef

def Get_coef_slau(tmp_coef):
	coef = []
	coef.append(coef_slau(0, 0, 0, 0))
	coef.append(coef_slau(0, 0, 0, 0))
	 
	N = len(tmp_coef) - 1
	
	for i in range(2, N + 1):

		a = tmp_coef[i-1].h
		b = -2 * (tmp_coef[i-1].h + tmp_coef[i].h)
		d = tmp_coef[i].h
		f = -3 * (tmp_coef[i].dyh - tmp_coef[i-1].dyh)
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

	for i in range(2, N-1):
		znam = slau[i].B - slau[i].A * ksi 

		eta = (slau[i].A * eta + slau[i].F) / znam
		ksi = slau[i].D / znam

		progon.append(Progon_coef(eta, ksi)) #i + 1

	return progon
def Get_interp_coef(c, tmp_coef, table):
	res = []
	N = len(table) - 1
	#print(len(c))
	res.append(interp_coef(0, 0, 0, 0))
	for i in range(1, N+1):
		#print(i)
		a = table[i - 1].y
		b = tmp_coef[i].dyh 
		b -= tmp_coef[i].h * (c[i+1] + 2 * c[i]) / 3
		d = (c[i+1] - c[i]) / (3 * tmp_coef[i].h)
		res.append(interp_coef(a, b, c[i], d))
		#print(res[-1])
	return res
	

def interp(table):
	#print(table)
	#print("len = ", len(table))
	tmp_coef = Get_temporary_coef(table)

	#print(tmp_coef)
	#print("len = ", len(tmp_coef))

	slau = Get_coef_slau(tmp_coef)

	#print(slau)
	#print("len = ", len(slau))

	progon = Get_progon_coef(slau)

	print(progon)
	print("len = ", len(progon))

	N = len(table) - 1

	c = []
	c.append(0)
	if(N >= 2): ##it is magic :)
		c.append((-slau[N].F - slau[N].A * progon[N].eta) / (-slau[N].B + slau[N].A * progon[N].ksi))
	else: 
		c.append(0)
	for i in range(N, 0, -1):
		c.append(progon[i].ksi * c[-1] + progon[i].eta)
	#c.append(0)
	c = c[::-1]

	#print(c)
	#print("len = ", len(c))

	res = Get_interp_coef(c, tmp_coef, table)

	return res

def fi(x, table, coef_interp):
	def binpoisk(x):
		a = 0
		b = len(table) - 1
		while(b - a > 1):	   
			m = int((a + b) / 2)
			if table[m].x > x:
				b = m
			elif table[m].x == x:
				return m
			else:
				a = m
		return a
	i = binpoisk(x) + 1
	dx = x - table[i-1].x
	y = coef_interp[i].a + dx * (coef_interp[i].b + dx * (coef_interp[i].c + dx * coef_interp[i].d)) 
	return y

def print_spline(table, coef_interp, f):
	def f_by_coef(coef, dx):
		y = coef.a + dx * (coef.b + dx * (coef.c + dx * coef.d))
		return y 

	import numpy as np
	import matplotlib.pyplot as plt
	x = np.linspace(table[0].x, table[-1].x, 100)
	y = []
	i = 0
	for xi in x:
		if(i == len(table)):
			break
		y.append(f_by_coef(coef_interp[i], xi - table[i-1].x))
		if(xi > table[i].x):
			i += 1
	plt.plot(x[5:], y[5:])
        #print(x)
	#print(y)
	##y = [f(i) for i in x]
 	#plt.plot(x, y)

 	#x1 = [a.x for a in table]
	#y1 = [a.y for a in table]

	#plt.plot(x1, y1, color = 'red')
	x2 = np.linspace(table[0].x, table[-1].x, 100)
	y2 = [f(i) for i in x2]
	plt.plot(x2, y2, color = 'green')

	plt.axis([table[0].x - 1, table[-1].x + 1, min(y) - 1, max(y) + 1])

	plt.show()
	return 

table = generate_table(f_0, -5, -4, 1)
#table = table_from_wiki()
coef_interp = interp(table)
#print_spline(table, coef_interp, f_0)

x = float(input("x = "))
y = fi(x, table, coef_interp)

print("Результат ", y)
print("Правильный ответ ", f_0(x))

