# SyoungCode.github.io

Sebastian Young's personal site: portfolio, CV, a live GitHub project feed, a SQL-backed data
dashboard, and a set of interactive ML demos — built one phase at a time.

**Live site:** https://syoungcode.github.io *(once GitHub Pages is switched on — see below)*

## Repo layout

This is one repo covering the whole project. Only `docs/` is served as the public website;
everything else is source code and notes for the phases that aren't live yet.

```
SyoungCode.github.io/
├── docs/            → the website itself (GitHub Pages serves this folder directly)
│   ├── index.html
│   ├── about.html
│   ├── projects.html
│   ├── dashboard.html
│   ├── ml-lab.html
│   ├── contact.html
│   ├── css/style.css
│   ├── js/github.js
│   └── assets/      → drop your CV PDF and a headshot/photo here
├── api/             → FastAPI backend (Phase 3) — empty for now
├── database/        → Olist schema + seed scripts (Phase 4) — empty for now
├── ml/              → training notebooks/scripts per ML project (Phase 5) — empty for now
├── writeups/        → short write-up per project, one per ML project (Phase 6)
└── .gitignore
```

## Why `docs/` and not `frontend/`

GitHub Pages can only serve a repo's root folder or its `/docs` folder — not an arbitrary
folder like `/frontend`. Naming the site folder `docs/` means Pages works with zero extra
config: just point Settings → Pages at the `docs` folder on `main` and it's live.

## Build phases

This repo is being built in the order laid out in the project roadmap:

1. **Static shell** — all pages live, styled, navigable *(this commit)*
2. **GitHub integration** — Projects page pulls live repos via the GitHub API, client-side *(this commit)*
3. **Backend skeleton** — a bare FastAPI app deployed to Render, proving the deploy chain
4. **Database + dashboard** — Olist data in Postgres (Supabase), SQL-backed KPIs on the Dashboard page
5. **ML Lab** — wine quality model first (already trained), then an Olist-based prediction task
6. **Polish** — write-ups, mobile pass, optional custom domain

## Getting this live

```bash
cd path/to/Portfolio
git init
git add .
git commit -m "Initial site shell + GitHub project feed"
git branch -M main
git remote add origin https://github.com/SyoungCode/SyoungCode.github.io.git
git push -u origin main
```

Then on GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch →
Branch: `main` / folder: `/docs`**. The site goes live at `https://syoungcode.github.io`
within a minute or two.
