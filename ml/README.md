# ml/ — Phase 5

## Wine quality — live

There's no separate model file here on purpose. Training on this dataset (1,359 rows
after removing duplicates) takes about a second, so `api/main.py` trains a fresh
`RandomForestRegressor` from the public dataset every time the API starts up, instead
of keeping a `.joblib` file in sync with the code. See the "Phase 5" section of
`api/main.py` for the exact training code — same approach as your Project 1 notebook
(same dataset, same duplicate-dropping step), just running as a script instead of in
Colab.

Typical accuracy: mean absolute error around 0.45–0.5 quality points on held-out data —
in line with published results on this dataset.

## Olist — not started

A second model (e.g. predicting whether an order arrives late) using the same Olist
data from `../database/`. Needs Phase 4's database in place first, since it trains on
that data.
