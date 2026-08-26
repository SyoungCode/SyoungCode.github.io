# api/ — Phase 3

A minimal FastAPI app with one endpoint (`GET /api/ping`) that exists purely to prove the
deploy chain works before anything real gets built on top of it.

## Run it locally

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit http://127.0.0.1:8000/docs — FastAPI gives you a free interactive tester for every
endpoint, no frontend needed to check it works.

## Deploy to Render (free tier)

1. Sign up at [render.com](https://render.com) and connect your GitHub account.
2. **New → Web Service**, pick the `SyoungCode.github.io` repo.
3. Because this is a monorepo, set:
   - **Root Directory:** `api`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy. Render gives you a URL like `https://syoungcode-api.onrender.com`.
5. Visit `https://<your-render-url>/api/ping` — you should see
   `{"status": "ok", "message": "Backend is alive."}`.
6. Paste that URL into `docs/js/api-status.js` (there's a clearly marked line for it) so
   the Home page can show a live "backend: reachable" status.

**Free tier note:** this service sleeps after ~15 minutes of no traffic. The first request
after that takes 30–50 seconds to wake it back up — expected, not a bug.

## What comes next (Phase 4+)

- `GET /api/olist/*` — dashboard KPIs, once `../database/` exists
- `POST /api/ml/*` — predictions, once `../ml/` has a trained model to load
