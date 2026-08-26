# api/ — Phase 3

Empty for now. This becomes a small FastAPI app deployed to Render, with routes like:

- `GET /api/olist/*` — dashboard KPIs, queried from the Postgres database in `../database/`
- `POST /api/ml/*` — predictions from the trained models in `../ml/`

Deploy note: when this exists, set Render's **Root Directory** to `api/` so it builds just
this folder out of the monorepo.
