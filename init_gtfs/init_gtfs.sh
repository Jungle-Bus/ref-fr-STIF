#!/bin/bash

set -euvo pipefail

# Initialisation des données GTFS

## téléchargement du GTFS
wget https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM_gtfs.zip --no-verbose -O fr-idf_oif_stif.zip 2>&1

## dézip des fichiers
unzip fr-idf_oif_stif.zip -d gtfs

## préfixage des fichiers
cd gtfs && ../init_gtfs/rename.sh

## nettoyage des fichiers temporaires
cd ..
rm fr-idf_oif_stif.zip && rm -R gtfs
