#!/bin/bash

set -euvo pipefail

# État des lieux par réseau des lignes OSM à créer ou au tracé manquant

cd data

## ajout des infos OSM sur les lignes open data
qsv join --left ID_Line opendata_lines_referential.csv ref:FR:STIF lignes.csv \
  |qsv select line_id,ID_Line,code,ShortName_Line,network,NetworkName,operator,OperatorName,mode,TransportMode \
  |qsv sort -s NetworkName,OperatorName,ID_Line > merged_lines.csv
# /!\ on a parfois plusieurs lignes OSM pour une même ligne opendata

## extraction des lignes OSM avec un tracé déjà existant
cat osm_extract_lines.csv |qsv search -s shape '^$' -v |qsv select line_id > osm_lines_with_shape.csv

## analyse des lignes opendata
cd ../missing_in_osm && python3 missing_lines.py > ../data/missing.md
