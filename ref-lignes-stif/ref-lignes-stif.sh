#!/bin/bash

set -euvo pipefail

# Mise à jour de la liste des lignes pour ref-lignes-stif
cd data 

cat osm_extract_lines.csv \
 |qsv search -s network TGV -v |qsv search -s network InOui -v  \
 |qsv search -s network Eurostar -v |qsv search -s operator 'Deutsche Bahn' -v \
 |qsv search -s network Thalys -v |qsv search -s network Flixbus -v \
 |qsv search -s network Intercités -v|qsv search -s operator 'SNCF Réseau' -v \
 |qsv search -s network 'TER ' -v |qsv search -s operator 'DB Fernverkehr' -v \
 |qsv search -s mode 'ferry' -v |qsv search -s mode 'walking_bus' -v \
 |qsv search -s mode 'construction' -v \
 |qsv search -s network 'local' -v |qsv search -s operator 'VTNI' -v \
  |qsv search -s operator 'Keolis Oise' -v |qsv search -s operator 'Transdev Oise CABARO' -v \
 |qsv search -s network 'Open Tour' -v | qsv search -s network 'Oise Mobilité' -v \
 |qsv search -s network 'Les Abeilles' -v | qsv search -s network 'Navettes Aéroports De Paris' -v \
 |qsv search -s network 'TransCape' -v | qsv search -s network Balabus -v \
 |qsv search -s network 'Big Bus' -v| qsv search -s network 'Carré 92' -v \
 |qsv search -s network 'Vexin Bus' -v | qsv search -s network "Transport à la Demande de Marne-la-Vallée" -v \
 |qsv select line_id,code,name,network,operator,colour,mode,ref:FR:STIF > lignes.csv

