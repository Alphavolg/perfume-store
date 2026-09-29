# باغ‌عطر — Persian perfume store homepage

- `src/style.css` + `build.py` are the single source for the homepage.
- `python3 build.py` generates:
  - `wp-content/themes/bagh-atr/` — a WordPress block theme (RTL). Zip this folder and upload it under Appearance > Themes; the homepage is `templates/front-page.html`.
  - `public/` — a static export of the same homepage, deployed on Vercel (Vercel cannot run PHP/MySQL, so the live WordPress runtime needs separate hosting).
- All product names, prices, reviews and contact details are sample content.
