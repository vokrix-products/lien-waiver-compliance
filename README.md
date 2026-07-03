# Lien Waiver Compliance

A construction lien waiver compliance extraction tool for small general contractors. Upload lien waiver PDFs, extract key fields, validate completeness, and flag missing or conditional waivers before payment release.

## Architecture

- **Extraction archetype**: buyer uploads files, poller processes, records table populated, dashboard shows results
- **Subdomain**: liens

## Repository Structure

- `extractor.py` — Calls Anthropic Claude Haiku to extract structured data from lien waiver text
- `validator.py` — Validates extracted fields and computes compliance status
- `pdf_reader.py` — Extracts plain text from PDF using pypdf
- `run_demo.py` — Offline demo with hardcoded test data
- `backend/poller.py` — Long-running poller that processes pending jobs via Supabase REST API
- `dashboard/` — Vite React dashboard for viewing waiver status

## Deployment

- GitHub repo: `vokrix-products/lien-waiver-compliance`
- Vercel project: `lien-waiver-compliance` (team `vokrix-s-projects`)
- Environment variables: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`