"""
Q5 – Functions, Parameters and Scope (College Canteen Order System)
Course: CSA0809 - Python Programming
Student: Y. Siva Pardhav (192412612)
"""

def add_item_buggy(item, order=[]):
    """
    Buggy version: Uses a mutable list as a default argument.
    The default list is created ONCE when the function is defined, not when called.
    """
    order.append(item)
    return order

def add_item(item, order=None):
    """
    Corrected version: Uses None as default and initializes a fresh list internally.
    """
    # TODO 1: Create a new empty list when order is None, append the item and return the list
    if order is None:
        order = []
    order.append(item)
    return order

# Demonstration of Scope (Local, Global, Nonlocal)
global_var = "I am Global"

def scope_demo():
    local_var = "I am Local"
    
    def inner_func():
        nonlocal local_var
        local_var = "Modified Local (Nonlocal)"
    
    inner_func()
    return local_var

if __name__ == "__main__":
    print("--- 1. Default Argument Bug Demonstration ---")
    print("Buggy calls (items persist from previous calls):")
    print("Call 1:", add_item_buggy("Tea"))
    print("Call 2:", add_item_buggy("Vada"))  # 'Tea' persists unexpectedly!
    
    print("\nCorrected calls (independent orders):")
    print("Customer 1:", add_item("Tea"))
    print("Customer 2:", add_item("Vada"))  # Starts fresh!
    
    print("\n--- 2. Default Defaults Inspection ---")
    print("add_item_buggy.__defaults__:", add_item_buggy.__defaults__)
    
    print("\n--- 3. Scope Demonstration ---")
    print("Global variable:", global_var)
    print("Scope test result:", scope_demo())