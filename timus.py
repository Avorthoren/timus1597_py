"""
For https://acm.timus.ru/problem.aspx?space=1&num=1597
"""
import functools
import math
from typing import Tuple

MAX_FLOORS = 10**18
MAX_EGGS = MAX_FLOORS.bit_length()


@functools.lru_cache(maxsize=1000)
def factorial(n: int) -> int:
	return math.factorial(n)


# i-th element is a function that returns floors_n(x, i).
# Calculated as sum(binomial(x, i) for e in range(1, i+1))
_FLOORS_N_SIMPLE_CASE = (
	lambda: 0,
	lambda x: x,
	lambda x: (x + 1) * x // 2,
	lambda x: (x**2 + 5) * x // 6,  # enough for MAX_FLOORS == 1000
	lambda x: (x**2 - 3*x + 14) * (x + 1) * x // 24,
	lambda x: (x**4 - 5*x**3 + 25*x**2 + 5*x + 94) * x // 120,
	lambda x: (x**4 - 10*x**3 + 65*x**2 - 140*x + 444) * (x + 1) * x // 720,
	lambda x: (x**6 - 14*x**5 + 112*x**4 - 350*x**3 + 1099*x**2 + 364*x + 3828) * x // 5040,
	lambda x: (x**6 - 21*x**5 + 231*x**4 - 1295*x**3 + 5264*x**2 - 9604*x + 25584) * (x + 1) * x // 40320,
	lambda x: (x**8 - 27*x**7 + 366*x**6 - 2646*x**5 + 12873*x**4 - 31563*x**3 + 79064*x**2 + 34236*x + 270576) * x // 362880
)

# _FLOORS_N_CACHE[eggs - len(_FLOORS_N_SIMPLE_CASE)][tries - eggs] == floors_n(tries, eggs)
_FLOORS_N_CACHE = tuple([] for _eggs in range(len(_FLOORS_N_SIMPLE_CASE), MAX_EGGS+1))


def floors_n(tries: int, eggs: int) -> int:
	"""Total number of floors that can be checked with given number of eggs in
	given number of tries.
	"""
	# We can not break more eggs than there are tries.
	eggs = min(tries, eggs)

	# Get polynomial answer for small values of `eggs`.
	if eggs < len(_FLOORS_N_SIMPLE_CASE):
		return _FLOORS_N_SIMPLE_CASE[eggs](tries)

	# Get cache for given value of `eggs`.
	cache = _FLOORS_N_CACHE[eggs - len(_FLOORS_N_SIMPLE_CASE)]
	# Check if answer already calculated.
	d_tries = tries - eggs
	while len(cache) <= d_tries:
		# Answer is not cached. Cache list is too short - expand it.
		cache.append(None)
	cache_value = cache[d_tries]
	if cache_value is not None:
		return cache_value

	# Main case: recursive call.
	value = floors_n(tries, eggs-1) + floors_n(tries-1, eggs) - floors_n(tries-1, eggs-2)
	cache[d_tries] = value
	return value


def _get_tries_range(floors: int, eggs: int) -> Tuple[int, int]:
	"""Find `left` and `right` such that
	floors_n(left, eggs) < floors <= floors_n(right, eggs)
	for 0 < floors, 1 < eggs <= floors.bit_length().
	"""
	# # Naive approach
	# left, right = 0, 1
	# while floors_n(right, eggs) < floors:
	# 	left, right = right, right << 1
	# return left, right

	# More advanced method is based on the fact that:
	# floors_n(t, e) = (t^e - O(t^(e-1)) / (e!)
	_pow = 1 / eggs
	guess = round((factorial(eggs) * floors) ** _pow)
	step = max(1, round(guess / 5))

	# while-loops inside will never be iterated, because chosen step is enough,
	# but just in case...
	if floors_n(guess, eggs) < floors:
		left, right = guess, guess + step
		while floors_n(right, eggs) < floors:
			left, right = right, right + step
	else:
		left, right = max(0, guess - step), guess
		while floors_n(left, eggs) >= floors:
			left, right = max(0, left - step), left

	return left, right


def tries_n(floors: int, eggs: int) -> int:
	"""Get number of tries needed to check given number of floors having given
	number of eggs.
	"""
	# Best algorithm needs floors.bit_length() eggs.
	eggs = min(eggs, floors.bit_length())

	if eggs == 1:
		return floors

	left, right = _get_tries_range(floors, eggs)
	# Binary search
	while left + 1 < right:
		mid = (left + right) >> 1
		if floors_n(mid, eggs) < floors:
			left = mid
		else:
			right = mid

	return right


def main():
	while True:
		eggs, floors = map(int, input().split())
		if not eggs and not floors:
			break
		print(tries_n(floors, eggs))


if __name__ == "__main__":
	main()
