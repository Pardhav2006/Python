"""
Q1 – Decisions with Many Boundaries
Course: CSA0809 - Python Programming
Student: Y. Siva Pardhav (192412612)
"""

def check_subsidy_separate(units, has_ration_card, senior_member):
    """
    Evaluates subsidy eligibility using independent separate if statements.
    Demonstrates the multi-result bug when conditions overlap.
    """
    results = []
    if units <= 100:
        results.append("Full Subsidy")
    if 101 <= units <= 200 and has_ration_card:
        results.append("Partial Subsidy")
    if units > 200 or senior_member:
        results.append("Age Exemption / No Subsidy")
    return results

def check_subsidy_elif(units, has_ration_card, senior_member):
    """
    Evaluates subsidy eligibility using a mutually exclusive if-elif-else chain.
    Guarantees exactly one decision per household.
    """
    if units <= 100:
        return "Full Subsidy"
    elif 101 <= units <= 200:
        return "Partial Subsidy" if has_ration_card else "No Subsidy"
    else:
        return "Age Exemption Subsidy" if senior_member else "No Subsidy"

def check_subsidy_match(units, has_ration_card, senior_member):
    """
    Alternative Concept: Python 3.10+ match-case pattern matching.
    """
    match units:
        case u if u <= 100:
            return "Full Subsidy"
        case u if 101 <= u <= 200:
            return "Partial Subsidy" if has_ration_card else "No Subsidy"
        case u if u > 200 and senior_member:
            return "Age Exemption Subsidy"
        case _:
            return "No Subsidy"

if __name__ == "__main__":
    # Test cases covering normal and boundary values (100, 101, 200, 201 units)
    test_households = [
        (50, False, False, "Normal Low"),
        (100, False, False, "Boundary Lower Full"),
        (101, True, False, "Boundary Lower Partial (with Card)"),
        (101, False, False, "Boundary Lower Partial (no Card)"),
        (200, True, False, "Boundary Upper Partial (with Card)"),
        (201, False, False, "Boundary Upper Exemption Test (no Senior)"),
        (90, False, True, "Overlap Test (<=100 and Senior > 80)"),
        (250, False, True, "Upper Slab Senior Exemption Test")
    ]

    print("=" * 80)
    print(f"{'Description':<38} | {'Separate IF':<28} | {'IF-ELIF-ELSE':<20}")
    print("=" * 80)
    
    for units, ration, senior, desc in test_households:
        sep_res = check_subsidy_separate(units, ration, senior)
        elif_res = check_subsidy_elif(units, ration, senior)
        print(f"{desc:<38} | {str(sep_res):<28} | {elif_res:<20}")
    
    print("=" * 80)