# Coordinate manipulation with gdal ton convert between different coordinate systems

import os
import sys
import osgeo.osr as osr
import osgeo.ogr as ogr

def convert_CRS3035_to_WG84(N,E):
    # Define the source and target coordinate systems
    src_srs = osr.SpatialReference()
    src_srs.ImportFromEPSG(3035)
    tgt_srs = osr.SpatialReference()
    tgt_srs.ImportFromEPSG(4326)

    # Create a transform object to convert between the two coordinate systems
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)

    # Perform the transformation
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(N, E)
    point.Transform(transform)

    return point.GetX(), point.GetY()

# CRS3035RES200mN2029800E4252400
i = 0
with open('carreaux_200m_met_wgs84.csv', 'w') as dest_file:
    with open('carreaux_200m_met.csv', 'r') as src_file:
        lines = src_file.readlines()
        dest_file.write(lines[0])
        lines = lines[1:]
        for line in lines:
            values = line.split(',')
            N = float(values[0][15:22])
            E = float(values[0][23:30])
            wgs84 = convert_CRS3035_to_WG84(N,E)
            dest_file.write(f"{wgs84[0]},{wgs84[1]},{','.join(values[1:len(values)])}")

            i += 1
            if i % 1000 == 0:
                print(f'Processed {i} lines')
