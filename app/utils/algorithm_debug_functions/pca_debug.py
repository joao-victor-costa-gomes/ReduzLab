def print_pca_parameters(params):
    """
    Prints a formatted summary of the validated PCA parameters for debugging.
    """
    print("\n--- PCA DEBUG: Validated Parameters Received ---")
    
    if not params:
        print("  No parameters received (likely a validation error occurred).")
        return

    for key, value in params.items():
        print(f"  - {key}: {value} (type: {type(value).__name__})")
        
    print("------------------------------------------------\n")