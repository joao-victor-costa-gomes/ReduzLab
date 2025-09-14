def print_kpca_parameters(params):
    print("\n--- KPCA DEBUG: Validated Parameters Received ---")
    
    if not params:
        print("  No parameters received (likely a validation error occurred).")
        return

    for key, value in params.items():
        print(f"  - {key}: {value} (type: {type(value).__name__})")
        
    print("--------------------------------------------------\n")