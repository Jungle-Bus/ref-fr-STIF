# Audit comparatif OSM / STIF

Ce répertoire contient le code, ainsi que les sauvegardes de données pour réaliser les audits comparatifs entre les données OSM et les données opendata du STIF.

En particulier, afin de gommer les divergences de modélisation, en complément des arrêts, on travaillera également sur des routepoints.

Un routepoint est un object logique qui représente un arrêt desservi par une ligne dans une direction.

Ces routepoints sont précalculés à partir des données OSM et GTFS à l'aide du factfile.

![processus](audit_routepoints.png)

# Pour lancer le notebook
## installation

L'audit utilise geopandas et une de ses dépendances rtree.

Si l'erreur `Could not find libspatialindex_c library file` se produit, installer le package libspatialindex-dev :  `apt install libspatialindex-dev`

L'audit utilise pipenv pour gérer ces dépendances. Il faut l'initialiser avec un `pipenv install`

## Lancement depuis un environnement virtuel

Pour naviguer dans les notebook de l'audit : `pipenv run jupyter notebook`

Ne pas oublier de modifier les répertoires d'entrée et de sortie en fonction du cas d'usage.
