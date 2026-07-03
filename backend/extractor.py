import os
import json
import requests

def extract_fields(text: str, filename: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"waiver_type": "unknown", "amount": "", "vendor": "", "project": "",
                "waiver_date": "", "through_date": "", "signed": "", "parse_error": True}
    
    prompt = (
        "Extract structured data from this lien waiver document. "
        "Return ONLY a JSON object with these keys: "
        "\"waiver_type\" (exactly \"conditional\" or \"unconditional\" or \"unknown\"), "
        "\"amount\" (numeric string or empty), "
        "\"vendor\" (subcontractor/supplier name or empty), "
        "\"project\" (project name or empty), "
        "\"waiver_date\" (ISO date YYYY-MM-DD or empty), "
        "\"through_date\" (good-through date ISO or empty), "
        "\"signed\" (\"yes\" or \"no\"). "
        "If the document appears signed, set signed to \"yes\".\n\n"
        "Document text:\n" + text
    )
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        content_blocks = data.get("content", [])
        if not content_blocks:
            raise ValueError("No content blocks")
        text_response = content_blocks[0].get("text", "")
        result = json.loads(text_response)
        result["parse_error"] = False
        return result
    except Exception:
        return {"waiver_type": "unknown", "amount": "", "vendor": "", "project": "",
                "waiver_date": "", "through_date": "", "signed": "", "parse_error": True}
