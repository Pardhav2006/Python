"""
Q3 – Engineer a Vehicle Registration Number Validator
Course: CSA0809 - Python Programming
Student: Y. Siva Pardhav (192412612)
"""

def normalised(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    # TODO 1: Remove spaces and hyphens and convert to upper case using string methods
    return text.replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    # TODO 2: Check the length is 9 or 10, then check each part using slicing with isalpha() and isdigit()
    if len(reg) == 9:
        # Format: LL DD L DDDD (Length 9)
        return (reg[0:2].isalpha() and 
                reg[2:4].isdigit() and 
                reg[4:5].isalpha() and 
                reg[5:9].isdigit())
    elif len(reg) == 10:
        # Format: LL DD LL DDDD (Length 10)
        return (reg[0:2].isalpha() and 
                reg[2:4].isdigit() and 
                reg[4:6].isalpha() and 
                reg[6:10].isdigit())
    return False

def format_receipt(reg):
    """Formats a valid registration number as 'TN 09 AB 1234'."""
    clean = normalised(reg)
    if is_valid(clean):
        if len(clean) == 9:
            return f"{clean[0:2]} {clean[2:4]} {clean[4:5]} {clean[5:9]}"
        else:
            return f"{clean[0:2]} {clean[2:4]} {clean[4:6]} {clean[6:10]}"
    return "INVALID"

if __name__ == "__main__":
    # Test cases including valid and invalid formats
    test_inputs = ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]
    
    print("-" * 65)
    for raw in test_inputs:
        reg = normalised(raw)
        status = "valid" if is_valid(reg) else "INVALID"
        formatted = format_receipt(raw)
        print(f"{raw:15} -> {reg:11} {status} | Receipt: {formatted}")
    print("-" * 65)
    