# Deploy Instructions (Render + Vercel) — Quick Start

## Overview
1. Deploy backend to Render (free web service).
2. Deploy frontend to Vercel (free static site hosting).
3. Set ENV variables on Render:
   - `APP_SECRET_KEY` (random long secret)
   - `GEMINI_API_KEY` (place your Gemini API key here)
   - `DATABASE_URL` (optional; SQLite used by default)

## Backend (Render)
1. Create a new Web Service on Render, connect your GitHub repo (or deploy via manual).
2. Set build command: `pip install -r requirements.txt`
   Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
3. Add environment variables in Render dashboard:
   - `APP_SECRET_KEY=your_secret_here`
   - `GEMINI_API_KEY=your_gemini_key_here`
4. Deploy.

## Frontend (Vercel)
1. Create a new project, import repo.
2. Build command: `npm run build`
   Output directory: `dist`
3. In Vercel dashboard add env var (only if you need to call backend from frontend directly):
   - `VITE_API_BASE_URL=https://<your-backend>.onrender.com`
4. Deploy.

## Local Run (Backend)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn app:app --reload --port 8000
```

## Local Run (Frontend)
```bash
cd frontend
npm install
npm run dev
```

