# Lien Waiver Compliance

Construction lien waiver compliance extraction tool. Upload lien waiver PDFs; extract key fields, validate completeness, flag conditional or missing waivers before payment release.

## Architecture

- **Dashboard**: Vite + React (shadcn-admin template)
- **Backend**: Python poller that processes Supabase Storage uploads via Anthropic Claude Haiku
- **Database**: Supabase (jobs, records tables)

## Setup

1. Copy `.env.example` (not tracked) with `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `PRODUCT_ID`, `ANTHROPIC_API_KEY`
2. `pip install -r backend/requirements.txt`
3. `cd dashboard && npm install && npm run dev`
4. `python3 backend/poller.py`

## Deployment

Dashboard deployed on Vercel (rootDirectory: dashboard). Poller runs as a background worker.
