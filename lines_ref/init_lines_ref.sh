#!/bin/bash

set -euvo pipefail

# Extraction lines ref

cd data 

## Extraction focus open data
wget --quiet "https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=," -O opendata_lines_referential.csv

