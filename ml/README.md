# ml/ — Phase 5

Empty for now. One subfolder per project, e.g.:

```
ml/
├── wine-quality/   → training notebook + the .joblib file the API loads
├── olist-delivery/
└── ...
```

Each project's fitted model gets `joblib.dump()`'d here, then loaded by `api/` at startup
and served through a `/api/ml/<project>` endpoint.
