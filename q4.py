"""
Q4 – Building Long Text: + or join()?
Course: CSA0809 - Python Programming
Student: Y. Siva Pardhav (192412612)
"""

import time

# Generate 200,000 items as test parts
items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]

def build_plus(parts):
    """Builds string using repeated += concatenation inside a loop."""
    text = ""
    for p in parts:
        text += p + ";"
    return text

def build_join(parts):
    """TODO 1: Build the same text using a single str.join() call."""
    return ";".join(parts) + ";"

if __name__ == "__main__":
    print("--- Running String Building Performance Benchmark ---")
    
    # Benchmark repeated += operator
    start = time.perf_counter()
    a = build_plus(items)
    t_plus = time.perf_counter() - start
    
    # Benchmark single str.join() call
    start = time.perf_counter()
    b = build_join(items)
    t_join = time.perf_counter() - start
    
    # Results verification
    print(f"same text: {a == b} | length: {len(b)}")
    print(f"+= time: {t_plus:.4f} s | join time: {t_join:.4f} s")
    print(f"Speedup factor: {t_plus / t_join:.2f}x faster with join()")