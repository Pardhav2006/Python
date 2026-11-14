readings = [4.5, -60.0, 2.1, 8.9, 55.2, 5.0, 1.8, 7.2]

# 1. For loop with append
valid_f_loop = []
for c in readings:
    if -50 <= c <= 50:
        valid_f_loop.append((c * 9/5) + 32)

# 2. List comprehension with condition
valid_c = [c for c in readings if -50 <= c <= 50]
valid_f_comp = [(c * 9/5) + 32 for c in readings if -50 <= c <= 50]

# 3. map() and filter() with lambda
valid_f_map = list(map(lambda c: (c * 9/5) + 32, filter(lambda c: -50 <= c <= 50, readings)))

# 4. Alarm minutes (outside 2–8 °C, excluding sensor errors) using enumerate()
alarm_minutes = [minute for minute, c in enumerate(readings) if -50 <= c <= 50 and not (2 <= c <= 8)]

print("Valid Fahrenheit:", valid_f_comp)
print("Alarm Minutes:", alarm_minutes)