#!/bin/bash

set -euvo pipefail

# Initialisation des données OSM

## téléchargement des données OSM
wget --quiet http://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf

## extraction des infos de transport
osm_transit_extractor --dump-all-tags -i ile-de-france-latest.osm.pbf -o data

## nettoyage des fichiers temporaires
rm *.osm.pbf
