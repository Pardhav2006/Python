# Student register numbers registered for Elective A and Elective B
elective_a = {19241201, 19241202, 19241203, 19241204}
elective_b = {19241203, 19241204, 19241205, 19241206}

# 1. Clash Detection (Intersection: registered in both)
clashes = elective_a & elective_b

# 2. Exactly One Elective (Symmetric Difference)
exclusive_registrations = elective_a ^ elective_b

# 3. Total Unique Students (Union)
all_registered = elective_a | elective_b

print("Clashing Students:", clashes)
print("Exclusive Registrations:", exclusive_registrations)