# Audit comparatif OSM / STIF

:warning::construction: c'est pas fini ! :construction::warning:

Afin de gommer les divergences de modélisation, au lieu de considérer des arrêts, on travaillera également sur des routepoints.

Un routepoint est un object fictif qui représente un arrêt desservi par une ligne dans une direction.

Si deux lignes s'arrêtent à un arrêt, il est représenté par deux routepoints.

Schéma attendu pour les routepoints :
* un id d'arrêt
* un code de ligne (de parcours en fait)
* terminus de ligne (de parcours en fait)
* code STIF de la ligne
* code STIF de l'arrêt
* nom de l'arrêt
* des infos complémentaires sur l'arrêt (coordonnées, accessibilité, etc)
* des infos complémentaires sur l'arrêt (réseau, etc)

# Pour lancer le notebook 
## Lancement depuis un environnement virtual
Après avoir instancié unenvironnement virtuel (par exemple avec `pipenv shell`), il faut indiquer à jupyter le kernel à utiliser. Pour ce faire, executer :
`ipython kernel install --user --name=projectname`

Vous pouvez ensuite executer `jupyter notebook`

## En cas d'erreur sur libspatialindex_c
L'audit utilise geopandas et une de ses dépendances rtree. 
Si l'erreur `Could not find libspatialindex_c library file` se produit, installer le package libspatialindex-dev :  
`apt install libspatialindex-dev` 