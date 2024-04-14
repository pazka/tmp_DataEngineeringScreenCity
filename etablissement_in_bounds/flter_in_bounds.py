import os
import sys
import json
import shapely

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

with open(BASE_PATH+'/admin-departement.geojson', 'r') as bounds_file:
    json_file = json.load(bounds_file)
    bounds = json_file['features'][0]['geometry']['coordinates'][0]

bounds_as_tuples = []
for b in bounds:
    bounds_as_tuples.append((float(b[0]), float(b[1])))

bounds_polygon = shapely.geometry.Polygon(bounds_as_tuples)

i = 0
in_bounds = 0
# HEADER siren,dateCreationEtablissement,denominationUniteLegale,isOnePerson,X,Y,appearances
with open(BASE_PATH+'/etablissements_geoloc_cleaned_with_count.csv', 'r') as src_file:
    with open(BASE_PATH+'/etablissements_geoloc_cleaned_with_count_in_ssd.csv', 'w') as dest_file:
        header = src_file.readline()
        dest_file.write(header)

        line = src_file.readline()

        while line and len(line) > 0:
            i += 1
            data = line.split(',')
            E = float(data[4])
            N = float(data[5])

            if bounds_polygon.contains(shapely.geometry.Point(N, E)):
                in_bounds += 1
                dest_file.write(line)

            if (i % 10000 == 0):
                print(f'Processed {round(i/351337*100)}%, {i}/351337, {in_bounds} in bounds')
            line = src_file.readline()
