from typing import List

import pytest

"""
Alice and Bob work in a beautiful orchard.
There are N  apple trees in the orchard.
The apple trees are arranged in a row and they are numbered from 1 to N.
Alice is planning to collect all the apples from K consecutive trees and Bob is planning to collect all the apples from L consecutive trees.
They want to choose two disjoint segments (one consisting of K trees for Alice and the other consisting of L trees for Bob) so as not to disturb each other.
What is the maximum number of apples that they can collect? Write a function that given an array A consisting of N integers denating the number of apples on each apple tree in the row, and integers K and L denoting, respectively, thenumber of trees that Alice and Bob can choose when collecting, returns the maximum number of apples that can be collected by them, or -1 if there are no such intervals.
For example, given A =[6, 1,4,6,3,2,7,4], K=3, L=2, your function should return 24, because Alice can choose trees 3 to 5 and collect 4 + 6 + 3 = 13 apples, and Bob can choose trees 7 to 8 and collect 7 + 4 = 11 apples.
Thus, they will collect 13 + 11 = 24 apples in total, and that is the maximum number that can be achieved.
Given A = [10, 19, 15], K = 2, L = 2, your function should return -1, because it is not possible for Alice and Bob to choose two disjoint intervals.
Assume that: 
N is an integer within the range [2..600];
K and L are integers within the range [1..N-1];
each element of array A is an integer within the range [1..500];
"""

INVALID_SUM = -1
RESULT_MODULO = 10**9 + 7


class OrchardTask:

	@classmethod
	def _calculate_subarray_sums(cls, arr: List[int], size: int) -> List[int]:
		result = [INVALID_SUM] * len(arr)
		result[0] = sum(arr[0: size])
		for start in range(1, len(arr) - size + 1):
			result[start] = result[start - 1] - arr[start - 1] + arr[start + size - 1]
		return result

	@classmethod
	def _find_best_subarray_sums_from_index_to_end(cls, subarray_sums: List[int]) -> List[int]:
		result = [INVALID_SUM] * len(subarray_sums)
		for start in range(len(subarray_sums) - 1, -1, -1):
			current_subarray_sum = subarray_sums[start]
			result[start] = max(current_subarray_sum, result[start + 1] if (start + 1) < len(result) else INVALID_SUM)
		return result

	@classmethod
	def _solve_helper(cls, subarray_sums: List[int], size: int, other_best_subarray_sums: List[int]) -> int:
		best_result = INVALID_SUM
		for start in range(len(subarray_sums) - size):
			curr_subarray_sum = subarray_sums[start]
			other_best_subarray_sum_in_remaining_array = other_best_subarray_sums[start + size]
			curr_result = curr_subarray_sum + other_best_subarray_sum_in_remaining_array
			best_result = max(best_result, curr_result)
		return best_result

	@classmethod
	def solve(cls, arr: List[int], K: int, L: int) -> int:
		if K + L > len(arr):
			return INVALID_SUM

		subarray_sums_alice = cls._calculate_subarray_sums(arr=arr, size=K)
		subarray_sums_bob = cls._calculate_subarray_sums(arr=arr, size=L)

		best_subarray_sums_alice = cls._find_best_subarray_sums_from_index_to_end(subarray_sums=subarray_sums_alice)
		best_subarray_sums_bob = cls._find_best_subarray_sums_from_index_to_end(subarray_sums=subarray_sums_bob)

		result_alice_bob = cls._solve_helper(subarray_sums=subarray_sums_alice, size=K, other_best_subarray_sums=best_subarray_sums_bob)
		result_bob_alice = cls._solve_helper(subarray_sums=subarray_sums_bob, size=L, other_best_subarray_sums=best_subarray_sums_alice)

		result = max(result_alice_bob, result_bob_alice)
		return result % RESULT_MODULO


class TestOrchardTask:

	@pytest.mark.parametrize(
		'arr, K, L, expected',
		[
			([1, 1], 1, 1, 2),
			([1, 0, 1], 1, 1, 2),
			([6, 1, 4, 6, 3, 2, 7, 4], 3, 2, 24),
			([10, 19, 15], 2, 2, -1),
			([1, 2, 9, 9, 2, 1], 2, 2, 22),
			([4, 4, 1, 5, 5], 2, 2, 18),
			([1, 1, 4, 4, 1, 5, 5, 1, 1], 2, 2, 18),
			([1, 1, 1, 10, 0, 10, 1, 1, 1], 3, 3, 24),
			([4, 4, 5, 9, 1, 9], 3, 2, 28),
			([4, 4, 5, 9, 1, 9], 2, 3, 28),
			([5, 5, 1, 1, 1, 5, 0, 5], 3, 2, 20),
			([5, 5, 1, 1, 1, 5, 0, 5], 2, 3, 20),
			([5, 0, 5, 1, 1, 1, 5, 5], 3, 2, 20),
			([5, 0, 5, 1, 1, 1, 5, 5], 2, 3, 20),
		],
	)
	def test_solve(self, arr: List[int], K: int, L: int, expected: int):
		actual = OrchardTask.solve(arr=arr, K=K, L=L)
		assert actual == expected
