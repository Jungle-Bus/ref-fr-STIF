#!/bin/bash

cat osm-transit-extractor_lines.csv \
 |xsv select line_id,code,name,network,operator,colour,osm:type,mode,osm:ref:FR:STIF:ExternalCode_Line \
 |xsv search -s network TGV -v | xsv search -s network Eurostar -v \
 |xsv search -s network Thalys -v |xsv search -s network Flixbus -v \
 |xsv search -s network Intercités -v|xsv search -s operator 'SNCF Réseau' -v \
 |xsv search -s network 'TER ' -v |xsv search -s operator 'DB Fernverkehr' -v \
 |xsv search -s mode 'ferry' -v |xsv search -s network 'local' -v \
 |xsv search -s network 'Open Tour' -v | xsv search -s network Balabus -v \
 |xsv search -s network 'Les Abeilles' -v | xsv search -s network 'Navettes Aéroports De Paris' -v \
 |xsv search -s network 'TransCape' -v | xsv search -s network Balabus -v \
 |xsv search -s network 'Big Bus' -v
