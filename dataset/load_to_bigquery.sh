#!/usr/bin/env bash
# Loads the world population CSVs into BigQuery.
# Requirements: Google Cloud SDK installed (gcloud + bq), and `gcloud auth login` done.
# Usage:  ./load_to_bigquery.sh YOUR_PROJECT_ID [DATASET_NAME] [LOCATION]
set -euo pipefail

PROJECT="${1:?Give your GCP project ID as the first argument}"
DATASET="${2:-world_population}"
LOCATION="${3:-US}"

gcloud config set project "$PROJECT"

# Create the dataset (skips if it already exists)
bq --location="$LOCATION" mk --dataset --description "World population by continent, country, state and city" \
   "$PROJECT:$DATASET" 2>/dev/null || echo "Dataset $DATASET already exists, continuing..."

for T in continents countries states_provinces cities geo_features; do
  echo "Loading $T ..."
  bq load --replace --source_format=CSV --skip_leading_rows=1 --allow_quoted_newlines \
     "$PROJECT:$DATASET.$T" "$T.csv" "${T}_schema.json"
done

echo "Done. Row counts:"
bq query --use_legacy_sql=false --format=pretty "
SELECT 'continents' t, COUNT(*) n FROM \`$PROJECT.$DATASET.continents\` UNION ALL
SELECT 'countries', COUNT(*) FROM \`$PROJECT.$DATASET.countries\` UNION ALL
SELECT 'states_provinces', COUNT(*) FROM \`$PROJECT.$DATASET.states_provinces\` UNION ALL
SELECT 'cities', COUNT(*) FROM \`$PROJECT.$DATASET.cities\` UNION ALL
SELECT 'geo_features', COUNT(*) FROM \`$PROJECT.$DATASET.geo_features\`"
