# Resume AI App (Backend + Frontend)

This repository contains a FastAPI backend and a React (Vite) frontend for a Resume Analyzer + JD Optimizer app.

## Quick start (local)

### Backend
1. Create a virtual environment and install requirements:
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set your OPENAI_API_KEY and DATABASE_URL (Neon/Postgres).

3. Run the server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# open http://localhost:5173
```

## Deployment suggestions
- Backend: Render / Railway (set env vars in the service settings)
- Frontend: Vercel / Netlify
- Database: Neon / Supabase (Postgres)
