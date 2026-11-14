rows, cols = 3, 4

# BUG: Every row references the exact same list object in memory
bad = [[0] * cols] * rows  
bad[0][1] = 7

# TODO 1: Create a rows x cols grid of zeros using list comprehension so every row is distinct
good = [[0 for _ in range(cols)] for _ in range(rows)]
good[0][1] = 7

print("bad:", bad)
print("good:", good)
print("bad[0] is bad[1]:", bad[0] is bad[1])       # True (aliased)
print("good[0] is good[1]:", good[0] is good[1])   # False (independent rows)

# Tuples as dictionary keys (immutable and hashable)
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
print("Stop name:", stops[(13.0418, 80.2341)])