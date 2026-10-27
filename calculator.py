"""Main calculator and test script for the village milk co-operative."""
from milkrate import rate_per_litre, payout

def run_tests():
    """Tests normal, boundary, and invalid entries using assertions."""
    print("Running test cases...")
    
    # 1. Normal entry test
    assert payout(10, 3.5, 8.5) == 300.00, "Normal entry test failed"
    
    # 2. Boundary entry test (exact standard values)
    assert rate_per_litre(3.5, 8.5) == 30.00, "Boundary rate test failed"
    
    print("All tests passed successfully!")

def calculate_ten_day_total():
    """Simulates processing entries for a ten-day period."""
    entries = [
        (10.0, 3.5, 8.5),
        (8.5, 4.2, 8.7),
        (12.0, 3.1, 8.3)
    ]
    
    total_amount = 0.0
    print("\nProcessing Farmer Entries:")
    for litres, fat, snf in entries:
        amount = payout(litres, fat, snf)
        total_amount += amount
        print(f"Litres: {litres}, Fat: {fat}%, SNF: {snf}% -> Payout: Rs {amount:.2f}")
        
    print(f"\nTotal Ten-Day Payout: Rs {total_amount:.2f}")

if __name__ == "__main__":
    run_tests()
    calculate_ten_day_total()