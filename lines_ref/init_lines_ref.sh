#!/bin/bash

set -euvo pipefail

# Extraction lines ref

cd data 

## Extraction focus open data
wget --quiet "https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=," -O temp_opendata_lines_referential.csv

cat temp_opendata_lines_referential.csv |xsv sort -s ExternalCode_Line,ID_Line > opendata_lines_referential.csv

rm temp_opendata_lines_referential.csv
