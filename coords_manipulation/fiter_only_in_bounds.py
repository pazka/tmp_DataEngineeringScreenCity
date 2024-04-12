# Read the bouds in geojson format

# read the data in csv format
# thee coordinates are in the first column delimited by ","

# if the coordinates are in the bounds of the polygon, write the line in the output file
# if not, skip the line


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
with open(BASE_PATH+'/carreaux_200m_met_wgs84.csv', 'r') as src_file:
    with open(BASE_PATH+'/carreaux_200m_SSD_wgs84.csv', 'w') as dest_file:
        header = src_file.readline()
        dest_file.write(header)

        line = src_file.readline()

        while line and len(line) > 0:
            i += 1
            coordinates = line.split(',')[0].split(';')[1:3]
            N = float(coordinates[1])
            E = float(coordinates[0])

            if bounds_polygon.contains(shapely.geometry.Point(N, E)):
                in_bounds += 1
                print(f'{in_bounds}/{i} in bounds ! ')
                dest_file.write(line)

            if (i % 10000 == 0):
                print(f'Processed {round(i/2287885*100)}%, {i}/2287885')
            line = src_file.readline()
