"""Performance and scale testing script for Task 10."""
import time
from milkrate import payout

def generate_sample_data(n):
    """Generates n sample entries of (litres, fat, snf)."""
    return [(10.0, 3.5, 8.5) for _ in range(n)]

def measure_performance():
    sizes = [300, 6000, 150000]
    
    print("--- Performance and Execution Analysis ---")
    for size in sizes:
        entries = generate_sample_data(size)
        
        start_time = time.perf_counter()
        
        # Calculate total payout for all entries
        total = sum(payout(litres, fat, snf) for litres, fat, snf in entries)
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        print(f"Payments: {size:6d} | Time Taken: {elapsed_time:.6f} seconds | Total: Rs {total:.2f}")

if __name__ == "__main__":
    measure_performance()