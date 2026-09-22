# Pujiverse World Atlas

An interactive world population explorer by **Pujiverse**.

- A lit, rotating **3D globe** that unrolls into a flat map when you click it (toggle back any time).
- Drill down **World → Continent → Country → State/Province → City**, with a clickable breadcrumb trail.
- Population, male/female, births and deaths for every level, with a **2015–2025 timeline**, line charts and ▲/▼ change vs. the previous year.
- **Area and population density** for continents, countries, states and cities.
- **Oceans, seas, lakes and islands**: 1,437 features with area, bordering countries and continents.
- Map and lists stay in sync on hover; search covers 37,000+ places and water bodies.

## Run locally

It's a static site. Any static server works:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

(Opening `index.html` straight from disk won't load the data, because browsers block `fetch` on `file://`.)

## Project layout

| Path | What |
|---|---|
| `index.html` | The whole app (HTML, CSS, JS). Uses D3 v7 and topojson from cdnjs. |
| `data/` | Pre-built JSON the app loads: stats, places, boundaries, water bodies. |
| `dataset/` | The source dataset: CSVs, BigQuery schemas, loader script, sample queries, Excel workbook. |
| `pipeline/` | Scripts that rebuild `data/` and `dataset/` from the raw sources. |

## Load the dataset into BigQuery

```bash
cd dataset
./load_to_bigquery.sh YOUR_PROJECT_ID world_population US
```

## Data sources & notes

- **Country population, sex split, birth & death rates**: World Bank WDI (2015–2025).
- **Cities (15,000+ people), coordinates, first-level divisions**: GeoNames.
- **Country & state boundaries, lakes, seas, islands**: Natural Earth (public domain). Ocean areas: CIA World Factbook.
- **City areas**: Wikidata city limits, where recorded (about 12,500 cities).
- City and state male/female and births/deaths are **estimates** from national ratios and rates.
  State population counts only the listed cities of 15,000+. Earlier-year values for states and cities are
  scaled from the national World Bank trend and are labelled as estimated in the app.

## Deploy

- **GitHub Pages**: Settings → Pages → Deploy from branch → `main` / root. The `.nojekyll` file is included.
- **Vercel**: import the repo; no build step (Framework preset "Other", output directory `.`).

---
Contact: pujiverse@gmail.com
