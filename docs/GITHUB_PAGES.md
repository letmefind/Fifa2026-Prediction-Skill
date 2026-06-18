# GitHub Pages demo

This folder contains a **static demo** of the FIFA 2026 Prediction Engine dashboard.

## Live URLs

| Setup | URL |
|-------|-----|
| **Organization root** (`letmefind.github.io` repo) | `https://letmefind.github.io/` |
| **This project** (Pages from `/docs`) | `https://letmefind.github.io/Fifa2026-Prediction-Skill/` |

## Deploy to `https://letmefind.github.io/` (root)

1. Create or open the repository **`letmefind/letmefind.github.io`** on GitHub.
2. Copy everything from this `docs/` folder into the **root** of that repository:
   - `index.html`
   - `demo.css`
   - `demo.js`
   - (optional) `README_10_LANGUAGES.md`, `BETTING_GUIDE.md`
3. In that repo: **Settings → Pages → Build and deployment → Deploy from branch `main` / root**.
4. Wait 1–2 minutes. The demo will be at `https://letmefind.github.io/`.

## Deploy from this repository (project Pages)

1. Open **Settings → Pages** on `Fifa2026-Prediction-Skill`.
2. Source: **Deploy from a branch** → `main` → **`/docs`** folder.
3. Or use the included GitHub Actions workflow (`.github/workflows/pages.yml`).
4. Demo URL: `https://letmefind.github.io/Fifa2026-Prediction-Skill/`

## Why the demo is not functional

GitHub Pages serves static HTML/CSS/JS only. The real app needs:

- Python 3.11+
- FastAPI + uvicorn
- ELO / Poisson / Monte Carlo models
- API-Football or CSV for latest scores

The demo shows the **UI layout** and **sample numbers** so visitors understand the product before cloning the repo.
