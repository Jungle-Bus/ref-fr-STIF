#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ref_FR_STIF_arrets
import ref_FR_STIF_lignes

import xmltodict
import datetime
from copy import deepcopy


def create_osmose_xml_stops(errors):
    with open('osmose_issues_template.xml', 'r') as f:
        doc = xmltodict.parse(f.read())

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    doc['analysers']['@timestamp'] = now
    doc['analysers']['analyser']['@timestamp'] = now
    doc['analysers']['analyser']['class']['@item'] = "8042"
    doc['analysers']['analyser']['class']['@tag'] = "transport en commun"
    doc['analysers']['analyser']['class']['@id'] = "2" #set the class of the item here
    doc['analysers']['analyser']['class']['@level'] = "3"
    doc['analysers']['analyser']['class']['classtext']['@lang'] = "fr"
    doc['analysers']['analyser']['class']['classtext'][
        '@title'] = "tag obsolète sur un arrêt de transport en commun d'Île-de-France"

    for error in errors :
        current_osmose_error = deepcopy(doc['analysers']['analyser']['error'][1])
        current_osmose_error['@class'] = '2'
        current_osmose_error['node']['@id'] = error['id']
        current_osmose_error['location']['@lat'] = error['lat']
        current_osmose_error['location']['@lon'] = error['lon']
        current_osmose_error['text']['@lang'] = "fr"
        current_osmose_error['text']['@value'] = error['label']
        current_osmose_error['fixes']['fix']['node']['@id'] = error['id']
        current_osmose_error['fixes']['fix']['node']['tag']['@k'] = 'ref:FR:STIF'

        doc['analysers']['analyser']['error'].append(current_osmose_error)

    # remove the template errors
    del doc['analysers']['analyser']['error'][0]
    del doc['analysers']['analyser']['error'][0]

    return xmltodict.unparse(doc, pretty=True)


def create_osmose_xml_lines(errors):
    with open('osmose_issues_template.xml', 'r') as f:
        doc = xmltodict.parse(f.read())

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    doc['analysers']['@timestamp'] = now
    doc['analysers']['analyser']['@timestamp'] = now
    doc['analysers']['analyser']['class']['@item'] = "8042"
    doc['analysers']['analyser']['class']['@tag'] = "transport en commun"
    doc['analysers']['analyser']['class']['@id'] = "1"
    doc['analysers']['analyser']['class']['@level'] = "3"
    doc['analysers']['analyser']['class']['classtext']['@lang'] = "fr"
    doc['analysers']['analyser']['class']['classtext'][
        '@title'] = "tag manquant sur une relation route_master (ligne de transport en commun)"

    for error in errors:
        current_osmose_error = deepcopy(
            doc['analysers']['analyser']['error'][0])
        current_osmose_error['relation']['@id'] = error['id']
        current_osmose_error['location']['@lat'] = error['lat']
        current_osmose_error['location']['@lon'] = error['lon']
        current_osmose_error['text']['@lang'] = "fr"
        current_osmose_error['text']['@value'] = error['label']
        current_osmose_error['fixes']['fix']['relation']['@id'] = error['id']
        if 'fix' in error:
            current_osmose_error['fixes']['fix']['relation']['tag']['@k'] = error['fix'][0]['key'] if 'key' in error['fix'][0] else ''
            current_osmose_error['fixes']['fix']['relation']['tag']['@v'] = error['fix'][0]['value'] if 'key' in error['fix'][0] else ''
        else:
            del current_osmose_error['fixes']

        doc['analysers']['analyser']['error'].append(current_osmose_error)

    # remove the template errors
    del doc['analysers']['analyser']['error'][0]
    del doc['analysers']['analyser']['error'][0]

    return xmltodict.unparse(doc, pretty=True)



if __name__ == '__main__':
    stop_errors = ref_FR_STIF_arrets.generate_osmose_errors_for_stops()
    print("Il y a {} erreurs sur les arrêts".format(len(stop_errors)))

    xml = create_osmose_xml_stops(stop_errors)
    with open("../data/osmose_stops.xml", "w") as xml_out_file:
        xml_out_file.write(xml)

    lines_errors = ref_FR_STIF_lignes.generate_osmose_errors_for_lines()
    print("Il y a {} erreurs sur les lignes".format(len(lines_errors)))

    xml = create_osmose_xml_lines(lines_errors)
    with open("../data/osmose_lines.xml", "w") as xml_out_file:
        xml_out_file.write(xml)
