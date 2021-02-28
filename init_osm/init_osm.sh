#!/bin/bash

set -euvo pipefail

# Initialisation des données OSM

## téléchargement des données OSM
wget http://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf --no-verbose 2>&1

## extraction des infos de transport
osm_transit_extractor --dump-all-tags -i ile-de-france-latest.osm.pbf -o data

## nettoyage des fichiers temporaires
rm *.osm.pbf
