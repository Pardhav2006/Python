import random

# Generate 365 daily rainfall readings (mm)
random.seed(42)
rainfall = [random.choice([0, 0, 0, 5, 12, 25, 40, 0]) for _ in range(365)]

# 1. Weekly Totals using Slicing
weekly_totals = [sum(rainfall[i:i+7]) for i in range(0, len(rainfall), 7)]

# 2. Find wettest and driest weeks with their positions
wettest_week = weekly_totals.index(max(weekly_totals)) + 1
driest_week = weekly_totals.index(min(weekly_totals)) + 1

# 3. 7-Day Moving Average (Running Sum approach for O(n) efficiency)
window_size = 7
moving_averages = []
window_sum = sum(rainfall[:window_size])
moving_averages.append(window_sum / window_size)

for i in range(len(rainfall) - window_size):
    window_sum = window_sum - rainfall[i] + rainfall[i + window_size]
    moving_averages.append(window_sum / window_size)

# 4. List of Dry Days (0 mm)
dry_days = [idx for idx, val in enumerate(rainfall) if val == 0]

print(f"Total Days: {len(rainfall)}")
print(f"Dry Days Count: {len(dry_days)}")
print(f"Wettest Week: Week {wettest_week} ({max(weekly_totals)} mm)")
print(f"Driest Week: Week {driest_week} ({min(weekly_totals)} mm)")