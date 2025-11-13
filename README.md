# FilexFlow — From Scratch (Next.js + FastAPI, Lemon Squeezy)

0) What you get
- Next.js frontend, FastAPI backend
- CORS enabled, Dockerfile for Render
- LemonSqueezy checkout via links (paste into /pricing)

1) Local run
Frontend:
  cd frontend && npm i && npm run dev
Backend:
  cd backend && python3 -m venv .venv && source .venv/bin/activate
  pip install -e .  (or pip install fastapi uvicorn ... per pyproject)
  uvicorn app.main:app --reload --port 8000

2) Deploy
- API: Render → Web Service (Docker), root: backend/
- Web: Vercel → Project → root: frontend/
- Vercel env: NEXT_PUBLIC_API_BASE=https://api.filexflow.com
- DNS: www→Vercel CNAME, @→76.76.21.21, api→Render CNAME

3) Lemon Squeezy
- Create products ($0.50 file, $9.99/mo)
- Paste checkout links into frontend/src/app/pricing/page.tsx
