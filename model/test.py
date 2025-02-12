from model import predict_outfit

def test_predict_outfit():
    test_cases = [
        ("navy", "gray"),               # Known values (should work)
        ("black", "khaki"),             # Possibly known values; if not, default handling is triggered
        ("unknown_blazer", "gray"),     # Unknown blazer color
        ("navy", "unknown_pant"),       # Unknown pant color
        ("unknown_blazer", "unknown_pant"),  # Both unknown
        ("red", "black")                # Known values (if available)
    ]

    for blazer, pant in test_cases:
        print(f"Testing with blazer: '{blazer}', pant: '{pant}'")
        try:
            shirt, tie, shoe = predict_outfit(blazer, pant)
            print(f"  Predicted: Shirt: {shirt}, Tie: {tie}, Shoe: {shoe}")
        except Exception as e:
            print(f"  Error: {e}")
        print("-" * 20)

if __name__ == "__main__":
    test_predict_outfit()