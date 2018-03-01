# ref-fr-STIF
Des scripts pour le suivi de l'intégration des référentiels île-de-France Mobilités (ex STIF) dans OSM.

## Prérequis
* [factotum](https://github.com/snowplow/factotum)
* [osm-transit-extractor](https://github.com/CanalTP/osm-transit-extractor)
* [xsv](https://github.com/BurntSushi/xsv)

## Documentation
https://wiki.openstreetmap.org/wiki/WikiProject_France/Transports_en_%C3%8Ele-de-France#R.C3.A9f.C3.A9rences_opendata

## TODO
### Analyse Osmose sur les codes STIF
L'analyse Osmose sur les lignes a été rappatriée. Reste à réécrire celle sur les arrêts. Pour le moment, c'est [ici](https://github.com/nlehuby/OSM_snippets/)

### Audit comparatif des routepoints
TODO

## NB
Pour générer les images de documentation des process : `factotum dot ref-lignes-stif.factfile --output factotum.dot && dot -Tpng factotum.dot -o factotum.png`
