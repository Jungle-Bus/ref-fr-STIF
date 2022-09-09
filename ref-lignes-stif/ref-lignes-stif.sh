#!/bin/bash

set -euvo pipefail

# Mise à jour de la liste des lignes pour ref-lignes-stif
cd data 

cat osm-transit-extractor_lines.csv \
 |xsv search -s 'osm:service' 'international' -v \
 |xsv search -s network TGV -v |xsv search -s network InOui -v  \
 |xsv search -s network Eurostar -v |xsv search -s operator 'Deutsche Bahn' -v \
 |xsv search -s network Thalys -v |xsv search -s network Flixbus -v \
 |xsv search -s network Intercités -v|xsv search -s operator 'SNCF Réseau' -v \
 |xsv search -s network 'TER ' -v |xsv search -s operator 'DB Fernverkehr' -v \
 |xsv search -s mode 'ferry' -v |xsv search -s mode 'walking_bus' -v \
 |xsv search -s mode 'construction' -v \
 |xsv search -s network 'local' -v |xsv search -s operator 'VTNI' -v \
  |xsv search -s operator 'Keolis Oise' -v |xsv search -s operator 'Transdev Oise CABARO' -v \
 |xsv search -s network 'Open Tour' -v \
 |xsv search -s network 'Les Abeilles' -v | xsv search -s network 'Navettes Aéroports De Paris' -v \
 |xsv search -s network 'TransCape' -v | xsv search -s network Balabus -v \
 |xsv search -s network 'Big Bus' -v| xsv search -s network 'Carré 92' -v \
 |xsv search -s network 'Vexin Bus' -v | xsv search -s network "Transport à la Demande de Marne-la-Vallée" -v \
 |xsv select line_id,code,name,network,operator,colour,osm:type,mode,osm:ref:FR:STIF:ExternalCode_Line,osm:ref:FR:STIF > lignes.csv
