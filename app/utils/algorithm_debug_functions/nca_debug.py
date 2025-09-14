def print_nca_parameters(params):
    """
    Prints a formatted summary of the validated NCA parameters for debugging.
    """
    print("\n--- NCA DEBUG: Validated Parameters Received ---")
    
    if not params:
        print("  No parameters received (likely a validation error occurred).")
        return

    for key, value in params.items():
        print(f"  - {key}: {value} (type: {type(value).__name__})")
        
    print("------------------------------------------------\n")