"""
Q2 – Loops that Count Attempts (OTP Verification at a Bank Kiosk)
Course: CSA0809 - Python Programming
Student: Y. Siva Pardhav (192412612)
"""

def verify_otp_while(correct_otp="1234"):
    """
    Simulates OTP verification using a while loop.
    Blank entries do not consume an attempt.
    """
    print("\n--- Starting OTP Verification (WHILE Loop) ---")
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        otp = input(f"Attempt {attempts + 1}/3 - Enter OTP (or leave blank to skip): ").strip()
        
        # Blank entry handling
        if otp == "":
            print("→ Blank entry detected. This does not count as an attempt.")
            continue  # Skips incrementing attempts and loops back
        
        if otp == correct_otp:
            print("→ Access Granted! Welcome to your account.")
            break
        else:
            print("→ Incorrect OTP.")
            attempts += 1
    else:
        # Executed only if the loop finishes without hitting 'break'
        print("→ ACCOUNT LOCKED for 30 minutes due to 3 failed attempts.")

def verify_otp_for(correct_otp="1234"):
    """
    Simulates OTP verification using a for loop with range(3).
    Demonstrates the use of pass and manual attempt tracking.
    """
    print("\n--- Starting OTP Verification (FOR Loop) ---")
    max_attempts = 3
    failed_attempts = 0
    
    for attempt_num in range(1, max_attempts + 1):
        otp = input(f"Attempt {attempt_num}/{max_attempts} - Enter OTP (or leave blank): ").strip()
        
        if otp == "":
            print("→ Blank entry detected. Using pass statement.")
            pass  # Placeholder statement
            # Note: A standard for loop in range consumes an iteration unless managed
            continue
            
        if otp == correct_otp:
            print("→ Access Granted!")
            break
        else:
            print("→ Incorrect OTP.")
            failed_attempts += 1
            if failed_attempts >= max_attempts:
                print("→ ACCOUNT LOCKED for 30 minutes.")
                break
    else:
        print("→ For loop completed successfully.")

if __name__ == "__main__":
    # Run the while loop verification demo
    verify_otp_while(correct_otp="1234")