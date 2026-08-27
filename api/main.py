"""
Backend API for the portfolio site.

Three jobs, in the order they were built:
  1. /api/ping            — Phase 3: prove the deploy chain works (see api/README.md)
  2. /api/olist/kpis       — Phase 4: SQL-backed dashboard numbers from Postgres
  3. /api/ml/wine-quality  — Phase 5: a live prediction from a trained model

Run locally with:
    pip install -r requirements.txt
    uvicorn main:app --reload
Then open http://127.0.0.1:8000/docs for the free interactive API tester.
"""

import os

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import create_engine, text

app = FastAPI(title="Sebastian Young — Portfolio API")

ALLOWED_ORIGINS = [
    "https://syoungcode.github.io",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/ping")
def ping():
    return {"status": "ok", "message": "Backend is alive."}


@app.get("/")
def root():
    return {"message": "See /docs for the interactive API explorer."}


# ---------------------------------------------------------------------------
# Phase 4 — Data Dashboard (Olist)
#
# The database itself lives wherever DATABASE_URL points (Postgres on
# Supabase, per database/README.md). This API never stores a password —
# it just reads the connection string from an environment variable, which
# you set once in Render's dashboard (Environment tab), never in code.
# ---------------------------------------------------------------------------

def get_engine():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return None
    return create_engine(db_url)


@app.get("/api/olist/kpis")
def olist_kpis():
    engine = get_engine()
    if engine is None:
        # Honest, non-crashing response for "the database doesn't exist yet" —
        # see database/README.md for the two steps that turn this on.
        raise HTTPException(
            status_code=503,
            detail="Database not connected yet — see database/README.md to set it up.",
        )

    try:
        with engine.connect() as conn:
            total_orders = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar()
            total_revenue = conn.execute(
                text("SELECT SUM(payment_value) FROM order_payments")
            ).scalar()
            avg_review_score = conn.execute(
                text("SELECT AVG(review_score) FROM order_reviews")
            ).scalar()
            avg_delivery_days = conn.execute(
                text(
                    """
                    SELECT AVG(EXTRACT(EPOCH FROM (order_delivered_customer_date - order_purchase_timestamp)) / 86400)
                    FROM orders
                    WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL
                    """
                )
            ).scalar()
    except Exception as exc:  # noqa: BLE001 — surface a readable message, not a stack trace
        raise HTTPException(status_code=500, detail=f"Query failed: {exc}") from exc

    return {
        "total_orders": int(total_orders or 0),
        "total_revenue_brl": round(float(total_revenue or 0), 2),
        "avg_review_score": round(float(avg_review_score or 0), 2),
        "avg_delivery_days": round(float(avg_delivery_days or 0), 1),
    }


# ---------------------------------------------------------------------------
# Phase 5 — ML Lab: wine quality
#
# Trained once, right here, at startup — on the same small public dataset
# from your Project 1 (Cortez et al.). Training takes about a second, so
# there's no separate model file to keep in sync with the code.
# ---------------------------------------------------------------------------

WINE_DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/winequality-red.csv"
WINE_FEATURES = [
    "fixed acidity", "volatile acidity", "citric acid", "residual sugar",
    "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density",
    "pH", "sulphates", "alcohol",
]

wine_model = None

try:
    _df = pd.read_csv(WINE_DATA_URL).drop_duplicates()
    wine_model = RandomForestRegressor(n_estimators=200, random_state=42)
    wine_model.fit(_df[WINE_FEATURES], _df["quality"])
except Exception as exc:  # noqa: BLE001 — don't let a flaky download take the whole API down
    print(f"Wine model failed to train at startup: {exc}")


class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float


@app.post("/api/ml/wine-quality")
def predict_wine_quality(input: WineInput):
    if wine_model is None:
        raise HTTPException(status_code=503, detail="Model failed to load — try again shortly.")

    row = pd.DataFrame([[
        input.fixed_acidity, input.volatile_acidity, input.citric_acid,
        input.residual_sugar, input.chlorides, input.free_sulfur_dioxide,
        input.total_sulfur_dioxide, input.density, input.pH,
        input.sulphates, input.alcohol,
    ]], columns=WINE_FEATURES)
    prediction = wine_model.predict(row)[0]
    return {"predicted_quality": round(float(prediction), 2)}
