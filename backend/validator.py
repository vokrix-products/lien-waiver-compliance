def validate(extracted: dict) -> dict:
    signed = extracted.get("signed", "")
    waiver_type = extracted.get("waiver_type", "")
    amount = extracted.get("amount", "")
    vendor = extracted.get("vendor", "")
    waiver_date = extracted.get("waiver_date", "")
    project = extracted.get("project", "")

    missing_fields = []
    if not vendor:
        missing_fields.append("vendor")
    if not amount:
        missing_fields.append("amount")
    if not project:
        missing_fields.append("project")
    if not waiver_date:
        missing_fields.append("waiver_date")
    if not waiver_type or waiver_type == "unknown":
        missing_fields.append("waiver_type")

    if signed == "no":
        compliance_status = "missing_signature"
        summary = "Document is not signed. Payment should not be released without a signature."
    elif waiver_type == "unknown" or not amount or not vendor or not waiver_date:
        compliance_status = "incomplete"
        summary = "Required fields are missing. Cannot determine compliance without all key fields."
    elif waiver_type == "conditional":
        compliance_status = "conditional_hold"
        summary = "Conditional waiver requires careful review before payment release."
    else:
        compliance_status = "compliant"
        summary = "Unconditional signed waiver — all fields present. Compliant."

    return {
        "compliance_status": compliance_status,
        "missing_fields": missing_fields,
        "summary": summary
    }
