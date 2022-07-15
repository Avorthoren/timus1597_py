from functools import reduce
from operator import mul
import timeit


def with_lambda(lst):
	reduce(lambda x, y: x * y, lst)


def without_lambda(lst):
	reduce(mul, lst)


def forloop(lst):
	r = 1
	for x in lst:
		r *= x
	return r


a = range(50)
b = range(1, 50)
t = timeit.Timer("with_lambda(a)", "from __main__ import with_lambda,a")
print("with lambda:", t.timeit())
t = timeit.Timer("without_lambda(a)", "from __main__ import without_lambda,a")
print("without lambda:", t.timeit())
t = timeit.Timer("forloop(a)", "from __main__ import forloop,a")
print("for loop:", t.timeit())

t = timeit.Timer("with_lambda(b)", "from __main__ import with_lambda,b")
print("with lambda (no 0):", t.timeit())
t = timeit.Timer("without_lambda(b)", "from __main__ import without_lambda,b")
print("without lambda (no 0):", t.timeit())
t = timeit.Timer("forloop(b)", "from __main__ import forloop,b")
print("for loop (no 0):", t.timeit())
