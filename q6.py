"""
Q6 & Q7 – Recursion, Memoisation, Limits, and Iterative Redesign
Course: CSA0809 - Python Programming
Student: Y. Siva Pardhav (192412612)
"""

from functools import lru_cache
import sys
import time

# Global counter for naive recursion call tracking
calls = 0

def ways_naive(n):
    """Plain recursive approach - O(2^n) time complexity with exponential call counts."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    """Memoised recursive approach - O(n) time complexity using lru_cache."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_iterative(n):
    """
    Q7: Optimized Iterative Bottom-Up Redesign.
    Achieves O(n) time complexity and O(1) auxiliary space complexity.
    Eliminates stack overflow and RecursionError for large inputs like n = 1000.
    """
    if n <= 1:
        return 1
    prev, curr = 1, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr

if __name__ == "__main__":
    print("--- 1. Q6 Call Count Comparison (n = 25) ---")
    calls = 0
    res_naive = ways_naive(25)
    print(f"naive: {res_naive} | calls = {calls}")

    calls = 0
    res_memo = ways_memo(25)
    print(f"memo : {res_memo} | calls = {calls}")

    print("\n--- 2. Growth Investigation Table ---")
    print(f"{'Steps (n)':<10} | {'Naive Calls O(2^n)':<20} | {'Memoised Calls O(n)'}")
    print("-" * 55)
    for n_val in [10, 20, 25, 30]:
        calls = 0
        ways_naive(n_val)
        naive_c = calls
        
        ways_memo.cache_clear()
        calls = 0
        ways_memo(n_val)
        memo_c = calls
        print(f"{n_val:<10} | {naive_c:<20} | {memo_c}")

    print("\n--- 3. Q7 Iterative Redesign Test (n = 1000) ---")
    start_time = time.perf_counter()
    ans_1000 = ways_iterative(1000)
    elapsed = time.perf_counter() - start_time
    print(f"Iterative result for 1000 steps computed successfully!")
    print(f"Execution time: {elapsed:.6f} seconds | Stack Space: O(1)")
    
    # Explanation of RecursionError
    print("\n--- 4. Explanation of RecursionError at n = 1000 ---")
    print(f"Default Python recursion limit: {sys.getrecursionlimit()}")
    print("Calling ways_memo(1000) creates 1,000 nested call frames on the C stack,")
    print("exceeding the safety limit and triggering a RecursionError. The iterative")
    print("loop bypasses the call stack entirely, running in O(1) space.")