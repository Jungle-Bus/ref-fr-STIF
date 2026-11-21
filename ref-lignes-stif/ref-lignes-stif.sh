#!/bin/bash

set -euvo pipefail

# Mise à jour de la liste des lignes pour ref-lignes-stif
cd data 

cat osm_extract_lines.csv \
 |xan search -s network TGV -v |xan search -s network InOui -v  \
 |xan search -s network Eurostar -v |xan search -s operator 'Deutsche Bahn' -v \
 |xan search -s network Thalys -v |xan search -s network Flixbus -v \
 |xan search -s network Intercités -v|xan search -s operator 'SNCF Réseau' -v \
 |xan search -s network 'TER ' -v |xan search -s operator 'DB Fernverkehr' -v \
 |xan search -s mode 'ferry' -v |xan search -s mode 'walking_bus' -v \
 |xan search -s mode 'construction' -v \
 |xan search -s network 'local' -v |xan search -s operator 'VTNI' -v \
  |xan search -s operator 'Keolis Oise' -v |xan search -s operator 'Transdev Oise CABARO' -v \
 |xan search -s network 'Open Tour' -v | xan search -s network 'Oise Mobilité' -v \
 |xan search -s network 'Les Abeilles' -v | xan search -s network 'Navettes Aéroports De Paris' -v \
 |xan search -s network 'TransCape' -v | xan search -s network Balabus -v \
 |xan search -s network 'Big Bus' -v| xan search -s network 'Carré 92' -v \
 |xan search -s network 'Vexin Bus' -v | xan search -s network "Transport à la Demande de Marne-la-Vallée" -v \
 |xan select 'line_id,code,name,network,operator,colour,mode,"ref:FR:STIF"' > lignes.csv

