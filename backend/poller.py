import os
import time
import json
import requests
from datetime import datetime, timezone

import pdf_reader
import extractor
import validator

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", os.environ.get("SUPABASE_KEY", ""))
PRODUCT_ID = os.environ["PRODUCT_ID"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
}

def fetch_pending_jobs():
    url = f"{SUPABASE_URL}/rest/v1/jobs"
    params = {
        "status": "eq.pending",
        "job_type": "eq.process_upload",
        "product_id": f"eq.{PRODUCT_ID}",
        "select": "*",
        "limit": "5",
    }
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def update_job_status(job_id, status, **kwargs):
    url = f"{SUPABASE_URL}/rest/v1/jobs"
    params = {"id": f"eq.{job_id}"}
    payload = {"status": status}
    for k, v in kwargs.items():
        if v is not None:
            payload[k] = v
    r = requests.patch(url, headers=HEADERS, params=params, json=payload)
    r.raise_for_status()

def download_file(file_path):
    url = f"{SUPABASE_URL}/storage/v1/object/uploads/{file_path}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.content

def upload_result(job_id, data):
    path = f"{job_id}.json"
    url = f"{SUPABASE_URL}/storage/v1/object/results/{path}"
    r = requests.put(url, headers=HEADERS, data=json.dumps(data))
    r.raise_for_status()
    return path

def create_record(job, fields, compliance_status, missing_fields, summary, source_file_path):
    url = f"{SUPABASE_URL}/rest/v1/records"
    vendor = fields.get("vendor", "")
    project = fields.get("project", "")
    if vendor and project:
        title = f"{vendor} - {project}"
    else:
        title = job.get("file_path", job.get("input_file_path", "unknown"))
    details = {
        "waiver_type": fields.get("waiver_type"),
        "amount": fields.get("amount"),
        "vendor": vendor,
        "project": project,
        "waiver_date": fields.get("waiver_date"),
        "through_date": fields.get("through_date"),
        "signed": fields.get("signed"),
        "missing_fields": missing_fields,
        "summary": summary,
    }
    payload = {
        "product_id": PRODUCT_ID,
        "customer_id": job.get("customer_id"),
        "title": title,
        "status": compliance_status,
        "details": details,
        "source_file_path": source_file_path,
        "due_date": fields.get("through_date") or None,
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    r.raise_for_status()

def process_job(job):
    job_id = job["id"]
    file_path = job.get("file_path") or job.get("input_file_path")
    if not file_path:
        raise ValueError("No file_path or input_file_path in job")
    update_job_status(job_id, "processing")
    pdf_bytes = download_file(file_path)
    text = pdf_reader.extract_text(pdf_bytes)
    if not text:
        raise ValueError("Empty PDF text")
    os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
    fields = extractor.extract_fields(text, file_path)
    result = validator.validate(fields)
    compliance_status = result["compliance_status"]
    missing_fields = result["missing_fields"]
    summary = result["summary"]
    create_record(job, fields, compliance_status, missing_fields, summary, file_path)
    result_path = upload_result(job_id, {"compliance_status": compliance_status, "summary": summary})
    update_job_status(
        job_id,
        "completed",
        output_file_path=result_path,
        result_summary={"compliance_status": compliance_status, "summary": summary},
        completed_at=datetime.now(timezone.utc).isoformat(),
    )

def main():
    while True:
        try:
            jobs = fetch_pending_jobs()
            for job in jobs:
                try:
                    process_job(job)
                except Exception as e:
                    job_id = job["id"]
                    try:
                        update_job_status(
                            job_id,
                            "failed",
                            error_message=str(e)[:500],
                        )
                    except Exception:
                        pass
        except Exception as e:
            print(f"Poll cycle error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
