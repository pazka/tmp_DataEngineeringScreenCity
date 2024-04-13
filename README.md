# Data engeeering SSD project

## Objective

Aggregation, cleaning and formating of all the data relating to Sein-Saint-Denis in preparation of a usage for DataVisuV2 for the art piece "ScreenCity"

## Data sources

|file|source|coordinates systems
|---|---|---|
|sirene of seine saint denis files extraction in 2019 | <https://www.sirene.fr/sirene/public/creation-fichier>|
|All sirene geolocalisation (32 Million lines) | <https://www.data.gouv.fr/fr/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/>|RGF93 Lambert 93 => WGS 84
|Population density of 2019 | <https://www.geoportail.gouv.fr/donnees/densite-de-population> Or <https://www.insee.fr/fr/statistiques/7655515>|CRS3035
|Contour administratifs Departements | <https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/#/resources>| CRS84
| COntour villes | <https://www.data.gouv.fr/fr/datasets/contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches/> vers <https://www.icem7.fr/cartographie/un-fond-de-carte-france-par-commune-optimise-pour-le-web-et-lanalyse-statistique/> vers <https://mapshaper.org/?files=https://static.data.gouv.fr/resources/contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches/20201115-141106/a-com2020.zip>|EPSG:3857

## Projection conversion with ogr2ogr

```bash
ogr2ogr -f GeoJSON -s_srs <my_file>.prj -t_srs EPSG:2154 <myfile>.geojson <my_file>.shp
```

EPSG coordinate gotten form <https://fr.wikipedia.org/wiki/Syst%C3%A8me_de_coordonn%C3%A9es_(cartographie)#Les_codes_EPSG>

## Population density

The coordinate is that of the bottom left corner of the square
