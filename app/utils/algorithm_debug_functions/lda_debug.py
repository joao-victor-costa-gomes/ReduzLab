def print_lda_parameters(params):
    """
    Prints a formatted summary of the validated LDA parameters for debugging.
    """
    print("\n--- LDA DEBUG: Validated Parameters Received ---")
    
    if not params:
        print("  No parameters received (likely a validation error occurred).")
        return

    for key, value in params.items():
        print(f"  - {key}: {value} (type: {type(value).__name__})")
        
    print("------------------------------------------------\n")