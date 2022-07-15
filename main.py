import functools
import math
import random
import time
from typing import Callable


Floors_N_Func_T = Callable[[int, int], int]


@functools.cache
def floors_n_recursive(tries: int, eggs: int) -> int:
	"""Total number of floors that can be checked with given number of eggs in
	given number of tries. Recursive approach.
	"""
	if tries < 0 or eggs < 0:
		raise ValueError

	# We can not break more eggs than there are tries.
	eggs = min(tries, eggs)

	if not tries or not eggs:
		return 0

	if tries == 1 or eggs == 1:
		return tries

	return sum(
		floors_n_recursive(t, eggs-1) + 1
		for t in range(tries)  # 0..tries-1
	)


# Fix signature, because functools.cache broke it.
floors_n_recursive: Floors_N_Func_T


def floors_n(tries: int, eggs: int) -> int:
	"""Total number of floors that can be checked with given number of eggs in
	given number of tries. Straightforward approach.
	"""
	if tries < 0 or eggs < 0:
		raise ValueError

	# We can not break more eggs than there are tries.
	eggs = min(tries, eggs)

	if not tries or not eggs:
		return 0

	if tries == 1 or eggs == 1:
		return tries

	return sum(
		math.comb(tries, e)        # Binomial(tries, e)
		for e in range(1, eggs+1)  # 1..eggs
	)


def _get_tries_range(
	floors: int,
	eggs: int,
	floors_n_func: Floors_N_Func_T = floors_n
) -> tuple[int, int]:
	"""Find `left` and `right` such that
	floors_n(left, eggs) < floors <= floors_n(right, eggs)
	for 0 < floors, 1 < eggs <= floors.bit_length().

	Naive approach would be:
	left, right = 0, 1
	while floors_n(right, eggs) < floors:
		left, right = right, right << 1

	More advanced method is based on the fact that:
	floors_n(t, e) = (t^e - O(t^(e-1)) / (e!)
	"""
	_pow = 1 / eggs
	guess = round(math.factorial(eggs)**_pow * floors**_pow)
	step = max(1, round(guess / 5))

	# while-loops inside will never be iterated, because chosen step is enough,
	# but just in case...
	if floors_n_func(guess, eggs) < floors:
		left, right = guess, guess + step
		while floors_n_func(right, eggs) < floors:
			left, right = right, right + step
	else:
		left, right = max(0, guess - step), guess
		while floors_n_func(left, eggs) >= floors:
			left, right = max(0, left - step), left

	return left, right


def tries_n(
	floors: int,
	eggs: int,
	floors_n_func: Floors_N_Func_T = floors_n
) -> int:
	"""Get number of tries needed to check given number of floors having given
	number of eggs.
	"""
	if floors < 1 or eggs < 1:
		raise ValueError

	# Best algorithm needs floors.bit_length() eggs.
	eggs = min(eggs, floors.bit_length())

	if eggs == 1:
		return floors

	left, right = _get_tries_range(floors, eggs, floors_n_func)
	# Binary search
	while left + 1 < right:
		mid = (left + right) >> 1
		if floors_n_func(mid, eggs) < floors:
			left = mid
		else:
			right = mid

	return right


def test(
	floors_n_func: Floors_N_Func_T,
	n: int = 100,
	max_floors: int = 2**32-1
) -> None:
	time0 = time.perf_counter()
	for _ in range(n):
		floors = random.randint(1, max_floors)
		eggs = random.randint(1, max_floors)
		tries = tries_n(floors, eggs, floors_n_func)
		# print(tries)
	time1 = time.perf_counter()
	print(f"{time1 - time0} seconds for {n} tests")


def main():
	# test(floors_n)

	floors_n_func = floors_n
	floors = 10**18
	print(f"{floors.bit_length()=}")
	eggs = 8

	time0 = time.perf_counter()
	tries = tries_n(floors, eggs, floors_n_func)
	print(f"tries_n({floors=:_}, {eggs=}) = {tries}")
	time1 = time.perf_counter()
	print(f"dt = {time1 - time0}s")
	if floors_n_func == floors_n_recursive:
		print(floors_n_recursive.cache_info())

	# print("Floors for first egg:")
	# f = 0
	# for t in range(tries-1, 0, -1):
	# 	f += floors_n(t, eggs-1) + 1
	# 	print(f"{f:_}")
	# print(f"{floors_n(tries, eggs):_}")


if __name__ == "__main__":
	main()
