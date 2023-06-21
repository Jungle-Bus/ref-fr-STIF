#!/bin/bash

set -euvo pipefail

# Initialisation des données OSM

## téléchargement des données OSM
wget --quiet http://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf

## extraction des infos de transport
osmium tags-filter ile-de-france-latest.osm.pbf type=route_master type=route -o pt_data.osm.pbf
cd ci/prism
poetry run python prism/cli.py ../../pt_data.osm.pbf --outdir ../../data --config ../../init_osm/prism_config.json --loglevel=WARNING -csv 

## dézip des fichiers
unzip ../../data/as_csv.zip -d osm

## rajout des tags additionnels dans les fichiers
cd ./osm
xsv join line_id lines.csv id additional_tags.csv | xsv select 1-13,ref:FR:STIF > lines_.csv
mv lines_.csv lines.csv

xsv join stop_point_id stop_points.csv id additional_tags.csv |xsv select 1-7,ref:FR:STIF > stops.csv
mv stops.csv stop_points.csv

## renommage des fichiers
for file in *.csv
do
    mv $file osm_extract_$file
done

mv osm_extract* ../../../data

## nettoyage des fichiers temporaires
cd ..
rm -R osm
cd ../../data
rm as_csv.zip
cd ..
rm *.osm.pbf

