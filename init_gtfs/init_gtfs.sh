#!/bin/bash

set -euvo pipefail

# Initialisation des données GTFS

## téléchargement du GTFS
wget --quiet https://data.iledefrance-mobilites.fr/explore/dataset/offre-horaires-tc-gtfs-idfm/files/42392f08db7bc164011695a72d9aa206/download/ -O fr-idf_oif_stif.zip

## dézip des fichiers
unzip fr-idf_oif_stif.zip -d gtfs

## préfixage des fichiers
cd gtfs && ../init_gtfs/rename.sh

## nettoyage des fichiers temporaires
cd ..
rm fr-idf_oif_stif.zip && rm -R gtfs
