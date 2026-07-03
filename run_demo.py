import validator

def main():
    extracted1 = {
        "waiver_type": "conditional",
        "amount": "12500.00",
        "vendor": "ABC Concrete LLC",
        "project": "Downtown Office Tower",
        "waiver_date": "2025-03-15",
        "through_date": "2025-04-15",
        "signed": "yes"
    }
    result1 = validator.validate(extracted1)
    print("Case 1:")
    print("  compliance_status:", result1["compliance_status"])
    print("  summary:", result1["summary"])
    print()

    extracted2 = {
        "waiver_type": "unconditional",
        "amount": "8500.00",
        "vendor": "XYZ Plumbing Inc",
        "project": "Riverside Apartments",
        "waiver_date": "2025-02-28",
        "through_date": "",
        "signed": "no"
    }
    result2 = validator.validate(extracted2)
    print("Case 2:")
    print("  compliance_status:", result2["compliance_status"])
    print("  summary:", result2["summary"])
    print()

    print("DEMO OK")

if __name__ == "__main__":
    main()
