# Data pipeline

These scripts rebuild the files in `../data/` (used by the website) and `../dataset/` (CSV / Excel / BigQuery files).
Run them from this folder with Python 3 and Node 18+ (`npm i d3-geo mapshaper`).

## Inputs to download into this folder

| File | Source |
|---|---|
| `cities15000.txt` | https://download.geonames.org/export/dump/cities15000.zip |
| `admin1codes.txt` | https://download.geonames.org/export/dump/admin1CodesASCII.txt |
| `countryInfo.txt` | https://download.geonames.org/export/dump/countryInfo.txt |
| `admin1/` | Natural Earth 1:10m admin-1 states & provinces |
| `phys/` | Natural Earth 1:10m marine polygons, lakes, geography regions |
| `countries50.json`, `countries110.json` | `world-atlas@2` on npm |
| `wb_*.json` | World Bank API: SP.POP.TOTL, SP.POP.TOTL.MA.IN, SP.POP.TOTL.FE.IN, SP.DYN.CBRT.IN, SP.DYN.CDRT.IN (2015–2025) |
| `inputs/` | The Pujiverse CSVs and workbook (continents, countries, states_provinces, cities, geo_features) |

## Order

1. `build1.py` – match every city to GeoNames coordinates.
2. `build2.py` – link states/provinces to Natural Earth boundaries.
3. `build3.py` – tag boundaries by country and continent, then simplify with mapshaper into `admin1.json`.
4. `node area.mjs` – geodesic areas of boundaries, water bodies and islands.
5. `update_files.py` – add area and density columns to the dataset (city areas come from Wikidata, linked by GeoNames ID).
6. `build4.py` – write `core.json`, `places.json`, `world50.json`, `world110.json` for the website.

`features.json` and `water.json` are built from `geo_features.csv` plus Natural Earth outlines.
