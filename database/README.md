# database/ — Phase 4

All the code is done. Two things need your own account, since I can't create one for you:

## 1. Create a free Postgres database on Supabase

1. Sign up free at [supabase.com](https://supabase.com), create a new project.
2. Once it's ready: **Project Settings → Database → Connection string** (choose the
   "URI" format). Copy it — it looks like
   `postgresql://postgres:[YOUR-PASSWORD]@....supabase.co:5432/postgres`.
3. In Supabase's own **SQL Editor**, paste the contents of `schema.sql` and run it —
   this creates the four empty tables the dashboard needs.

## 2. Load the data

On your own machine (not this session — this step needs your real database password):

```bash
cd database
pip install -r requirements.txt
export DATABASE_URL="postgresql://...."   # the connection string from step 1
python seed.py
```

This downloads the four Olist CSVs it needs automatically (public mirrors, no Kaggle
account required) and loads them straight into your database. Takes under a minute.

## 3. Tell Render about it

Your API needs that same connection string to answer dashboard requests. On Render:
your service → **Environment** tab → add `DATABASE_URL` with the same value → save
(this triggers a redeploy automatically).

Once that's done, `GET /api/olist/kpis` on your deployed API will return real numbers,
and the Dashboard page will show them instead of "not connected yet."

## What's in here

- `schema.sql` — all nine tables from the real Olist dataset: `orders`, `order_items`,
  `order_payments`, `order_reviews`, `customers`, `products`, `sellers`, `geolocation`,
  and `product_category_name_translation`.
- `seed.py` — downloads all nine and loads them in (tested end to end before being
  handed to you). `geolocation` alone is about a million rows, so this step can take
  several minutes over the network — that's expected. See `queries.sql` for the four
  dashboard numbers it should produce: roughly 99,441 orders, ~R$16M total revenue,
  ~4.07 average review score, ~12.6 average delivery days.
- `queries.sql` — the exact SQL the API runs, so you can run it yourself in Supabase's
  editor and see it work independently of the website.

Only four of the nine tables (`orders`, `order_items`, `order_payments`, `order_reviews`)
feed the current dashboard — the other five (`customers`, `products`, `sellers`,
`geolocation`, `product_category_name_translation`) are loaded in and ready for whenever
you want to add more KPIs, like top product categories or orders by state.
