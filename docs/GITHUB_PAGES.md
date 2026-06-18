# GitHub Pages demo

Static preview of the FIFA 2026 Prediction Engine dashboard (sample data only).

## Live URL

After setup (below):

**https://letmefind.github.io/Fifa2026-Prediction-Skill/**

## One-time setup (fix for deploy errors)

If the GitHub Action failed or the site shows **404**, do this once:

1. Open **Settings → Pages** on the repository:  
   https://github.com/letmefind/Fifa2026-Prediction-Skill/settings/pages

2. Under **Build and deployment**:
   - **Source:** Deploy from a branch
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`

3. Save, then run the workflow manually:  
   **Actions → Deploy GitHub Pages demo → Run workflow**

4. Wait 1–2 minutes and open the live URL above.

The workflow pushes the `docs/` folder to the `gh-pages` branch. You do **not** need “GitHub Actions” as the Pages source.

## Root URL `https://letmefind.github.io/`

To host at the organization root, copy `docs/index.html`, `demo.css`, `demo.js`, and `.nojekyll` into the **`letmefind/letmefind.github.io`** repository root and enable Pages from `main`.

## Why the demo is not functional

GitHub Pages serves static HTML/CSS/JS only. Live predictions need Python, FastAPI, and the full engine — [install from GitHub](https://github.com/letmefind/Fifa2026-Prediction-Skill).
