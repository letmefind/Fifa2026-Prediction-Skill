# GitHub Pages demo

Static preview of the FIFA 2026 Prediction Engine dashboard — same layout as `http://127.0.0.1:8000/`, with sample data only.

## Live URL

**https://letmefind.github.io/Fifa2026-Prediction-Skill/**

## Why you might see the README instead of the dashboard

GitHub Pages was likely set to publish the **repository root** (`main` / `/`), which renders `README.md` as the homepage.

This repo fixes that in two ways:

1. **Root `index.html`** redirects to `docs/index.html` when Pages uses `main` / root.
2. **GitHub Action** publishes only the dashboard (`index.html`, `demo.css`, `demo.js`) to the **`gh-pages`** branch.

## Recommended setup (one time)

1. Open **Settings → Pages**:  
   https://github.com/letmefind/Fifa2026-Prediction-Skill/settings/pages

2. Under **Build and deployment**:
   - **Source:** Deploy from a branch
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`

3. Save, then run **Actions → Deploy GitHub Pages demo → Run workflow**.

4. Wait 1–2 minutes and open the live URL.

## Alternative: main / docs

If you prefer **Branch: `main`**, **Folder: `/docs`**, GitHub serves `docs/index.html` directly at the project URL. The root redirect is not used in that case.

## Full predictions (not on GitHub Pages)

GitHub Pages is static HTML only. Live ELO/Poisson forecasts, score refresh, and tournament simulation need Python + FastAPI:

```bash
uvicorn api.main:app --reload
# http://127.0.0.1:8000/
```

Or deploy the API to Render, Railway, Fly.io, etc., and point the dashboard at that backend.
