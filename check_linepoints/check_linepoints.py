#!/usr/bin/env python
# coding: utf-8

import csv
import math


opendata_lines = {}
with open('../data/temp_opendata_linepoints.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        if row['route_reference'] == '':
            continue        
        if row['route_reference'] not in opendata_lines:
            opendata_lines[row["route_reference"]] = []
        opendata_lines[row["route_reference"]].append(row['stop_reference'])

osm_lines = {}
with open('../data/temp_osm_linepoints.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        if row['line_ref:FR:STIF'] == '':
            continue
        if row['line_ref:FR:STIF'] not in osm_lines:
            osm_lines[row["line_ref:FR:STIF"]] = []
        if row['line_ref:FR:STIF'] not in opendata_lines:
            continue
        ok_refs = opendata_lines[row['line_ref:FR:STIF']]
        if row['stop_ref:FR:STIF'] not in ok_refs:
            continue
        osm_lines[row["line_ref:FR:STIF"]].append(row['stop_ref:FR:STIF'])

tt = []
with open('../data/lignes.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        nb_ref_opendata = None
        nb_ref_osm = None
        stop_completude = None
        if row["osm:ref:FR:STIF"] in opendata_lines:
            nb_ref_opendata = len(set(opendata_lines[row["osm:ref:FR:STIF"]]))
        if row["osm:ref:FR:STIF"] in osm_lines:
            nb_ref_osm = len(set(osm_lines[row["osm:ref:FR:STIF"]]))
        if nb_ref_osm and nb_ref_opendata:
            stop_completude = math.floor(nb_ref_osm *100/nb_ref_opendata)
            row["stop_completude"] = "{} % ({}/{})".format(stop_completude, nb_ref_osm,nb_ref_opendata )
        tt.append(row)

with open('../data/osm_lines_with_stop_ref_completude.csv', 'w') as out_file:
    csv_writer = csv.DictWriter(out_file, delimiter=',', fieldnames=tt[0].keys())
    csv_writer.writeheader()
    for row in tt:
        csv_writer.writerow(row)

