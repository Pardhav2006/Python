"""Adapted rate card of the village milk co-operative with seasonal revisions and bonus."""

# Constants for normal/default season
BASE_RATE_NORMAL = 30.00
FAT_STEP_VALUE_NORMAL = 0.40
SNF_STEP_VALUE_NORMAL = 0.30

# Constants for summer season (April to June)
BASE_RATE_SUMMER = 32.00
FAT_STEP_VALUE_SUMMER = 0.45

BONUS_THRESHOLD = 500.0
BONUS_AMOUNT = 0.50

def rate_per_litre(fat, snf, month=1):
    """Returns the price per litre based on fat, snf, and month (seasonal adjustment)."""
    # Seasonal check: April to June corresponds to months 4, 5, 6
    if 4 <= month <= 6:
        base_rate = BASE_RATE_SUMMER
        fat_step_val = FAT_STEP_VALUE_SUMMER
    else:
        base_rate = BASE_RATE_NORMAL
        fat_step_val = FAT_STEP_VALUE_NORMAL
        
    # With 2-decimal precision readings, step computation uses round()
    fat_steps = round((fat - 3.5) / 0.1, 2)
    snf_steps = round((snf - 8.5) / 0.1, 2)
    
    rate = base_rate + (fat_steps * fat_step_val) + (snf_steps * SNF_STEP_VALUE_NORMAL)
    return round(rate, 2)

def ten_day_payout(entries, month=1):
    """
    Calculates total payout for a 10-day period given a list of tuples: (litres, fat, snf).
    Applies a Rs 0.50 per litre bonus if total litres exceed 500[cite: 14].
    """
    total_litres = sum(entry[0] for entry in entries)
    base_total = 0.0
    
    for litres, fat, snf in entries:
        rate = rate_per_litre(fat, snf, month)
        base_total += litres * rate
        
    # Apply bonus if total litres supplied exceed 500[cite: 14]
    if total_litres > BONUS_THRESHOLD:
        bonus = total_litres * BONUS_AMOUNT
        base_total += bonus
        
    return round(base_total, 2)

if __name__ == "__main__":
    # Test case: Normal season vs Summer season (e.g., Month 5 = May)
    sample_entries = [(300.0, 4.25, 8.63), (250.0, 3.80, 8.50)]
    print("Normal Season Payout (Month 1):", ten_day_payout(sample_entries, month=1))
    print("Summer Season Payout (Month 5):", ten_day_payout(sample_entries, month=5))