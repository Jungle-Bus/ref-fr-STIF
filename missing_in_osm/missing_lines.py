#!/usr/bin/env python
# coding: utf-8

import csv

osm_with_shapes = []
with open("../data/osm_lines_with_shape.csv") as shapescsvfile:
    tt = csv.reader(shapescsvfile)
    for elem in tt:
        osm_with_shapes.append(elem[0])

lines = []
with open("../data/opendata_lines_with_osm_id.csv") as csvfile:
    csv_ = csv.DictReader(csvfile)
    for tt in csv_:
        line = {}
        line['opendata_line_id'] = tt['route_id']
        line['opendata_network'] = tt['agency_name']
        line['opendata_line_name'] = tt['route_short_name']
        line['found_in_osm'] = tt['line_id'] != ''
        line['osm_line_id'] = tt['line_id']
        line['has_shape_in_osm'] = tt['line_id'] in osm_with_shapes
        lines.append(line)

networks = list(set([line['opendata_network'] for line in lines]))

content = """
# État des lieux par réseau de l'open data IDFM

* les lignes comptabilisées dans OpenStreetMap sont celles qui ont une référence de ligne (ref:FR:STIF)
* les lignes sont considérées sans tracé si aucune de leurs relations route ne contient de chemin.
* Voir aussi les [erreurs Osmose](http://osmose.openstreetmap.fr/fr/issues/open?source=28482&item=8042)


"""
content += "Sur un total de {} lignes open data: \n".format(len(lines))
content += "- {} lignes sont manquantes dans OSM \n".format(len( [line for line in lines if not line['found_in_osm']]))
content += "- {} lignes restent à tracer dans OSM \n".format(len( [line for line in lines if not line['has_shape_in_osm']]))


for a_network in networks:
    content += "\n# {} \n".format(a_network)
    lines_of_this_network = [line for line in lines if line['opendata_network'] == a_network]
    content += "{} lignes open data \n".format(len(lines_of_this_network))

    osm_missing_lines_of_this_network = [line for line in lines_of_this_network if not line['found_in_osm']]
    content += "\n dont {} manquantes dans OSM \n \n".format(len(osm_missing_lines_of_this_network))

    if osm_missing_lines_of_this_network:
        for elem in osm_missing_lines_of_this_network:
            link = "https://me-deplacer.iledefrance-mobilites.fr/fiches-horaires/bus/resultat?line=line:IDFM:{}".format(elem['opendata_line_id'])
            content += " - {} : {} \n".format(elem['opendata_line_name'], link)

    osm_lines_of_this_network = [line for line in lines_of_this_network if line['found_in_osm']]
    osm_missing_shapes_of_this_network = [line for line in osm_lines_of_this_network if not line['has_shape_in_osm']]
    content += "\n\n dont {} lignes OSM sans tracé \n \n".format(len(osm_missing_shapes_of_this_network))

    if osm_missing_shapes_of_this_network:
        for elem in osm_missing_shapes_of_this_network:
            osm_link = "https://ref-lignes-stif.5apps.com/line.html?osm_relation={}".format(elem['osm_line_id'].split('r')[-1])
            link = "https://me-deplacer.iledefrance-mobilites.fr/fiches-horaires/bus/resultat?line=line:IDFM:{}".format(elem['opendata_line_id'])
            content += " - [{}]({}) : {} \n".format(elem['opendata_line_name'], link, osm_link )



print(content)
