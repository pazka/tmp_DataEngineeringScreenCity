# Read the bouds in geojson format

# read the data in csv format
# thee coordinates are in the first column delimited by ","

# if the coordinates are in the bounds of the polygon, write the line in the output file
# if not, skip the line


import os
import sys
import json
from PIL import Image, ImageDraw 
  
  
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

result = []
def debug_squares():
    """
    Debug the squares
    """
    image = Image.new('RGB', (1000, 1000), color = "white")
    draw = ImageDraw.Draw(image)

    max_x = 0 
    max_y = 0
    min_x = 10000
    min_y = 10000

    for square in result:
        for key in square:
            if square["x1"] > max_x:
                max_x = square["x1"]
            if square["y1"] > max_y:
                max_y = square["y1"]
            if square["x1"] < min_x:
                min_x = square["x1"]
            if square["y1"] < min_y:
                min_y = square["y1"]
    print(f'max_x: {max_x}, max_y: {max_y}, min_x: {min_x}, min_y: {min_y}')

    for square in result:
        draw.polygon([
            (int((square["x1"] - min_x) * 1000 / (max_x - min_x)), int((square["y1"] - min_y) * 1000 / (max_y - min_y))),
            (int((square["x2"] - min_x) * 1000 / (max_x - min_x)), int((square["y2"] - min_y) * 1000 / (max_y - min_y))),
            (int((square["x3"] - min_x) * 1000 / (max_x - min_x)), int((square["y3"] - min_y) * 1000 / (max_y - min_y))),
            (int((square["x4"] - min_x) * 1000 / (max_x - min_x)), int((square["y4"] - min_y) * 1000 / (max_y - min_y)))
        ], fill=(255, 255, 255), outline ="blue")
    image.show()

# TOP = Y Up
# BOTTOM = Y Down
# LEFT = X Down
# RIGHT = X Up

data_example = {
    "x1": 7.7645431599807, "y1": 48.512304035071,
    "x2": 7.76462328819277, "y2": 48.5105057114528,
    "x3": 7.76732808033652, "y3": 48.5105601888606,
    "x4": 7.767248048927, "y4": 48.5123585147297,
    "pop": 6
}
#bottom_left = x2
#bottom_right = x3
#top_right = x4
#top_left = x1

square_measurements = {
    "bottom_left" : {
        "x": 0,
        "y": 0
    },
    "bottom_right_from_bottom_left": {
        "x": data_example["x3"] - data_example["x2"],
        "y": data_example["y3"] - data_example["y2"]
    },
    "top_right_from_bottom_left": {
        "x": data_example["x4"] - data_example["x2"],
        "y": data_example["y4"] - data_example["y2"]
    },
    "top_left_from_bottom_left": {
        "x": data_example["x1"] - data_example["x2"],
        "y": data_example["y1"] - data_example["y2"]
    },
}

# csv header and data example
# HEADER : idcar_200m,idcar_1km,idcar_nat,i_est_200,i_est_1km,lcog_geo,ind,men,men_pauv,men_1ind,men_5ind,men_prop,men_fmp,ind_snv,men_surf,men_coll,men_mais,log_av45,log_45_70,log_70_90,log_ap90,log_inc,log_soc,ind_0_3,ind_4_5,ind_6_10,ind_11_17,ind_18_24,ind_25_39,ind_40_54,ind_55_64,ind_65_79,ind_80p,ind_inc
# DATA : WSG84;48.81084981739457;2.595169461739732,CRS3035RES1000mN2882000E3778000,CRS3035RES2000mN2882000E3778000,0,0,7737393051,109.5,38,2,5,4,37,5,2962132.9,3678,0,38,6,21,5,6,0,0,4,2,7.5,9,14,15,24,11,18,5,0


def get_square_coords_from_bottom_left_coords(x, y):
    """
    Get the coordinates of the 4 corners of the square from the bottom left corner
    """
    return {
        "x1": x,
        "y1": y,
        "x2": x + square_measurements["bottom_right_from_bottom_left"]["x"],
        "y2": y + square_measurements["bottom_right_from_bottom_left"]["y"],
        "x3": x + square_measurements["top_right_from_bottom_left"]["x"],
        "y3": y + square_measurements["top_right_from_bottom_left"]["y"],
        "x4": x + square_measurements["top_left_from_bottom_left"]["x"],
        "y4": y + square_measurements["top_left_from_bottom_left"]["y"]
    }


def convert_csv_line_to_json_object(line) -> dict:
    """
    Convert a csv line to a json object
    """
    data = line.split(',')
    coords = data[0].split(';')[1:]
    square_coords = get_square_coords_from_bottom_left_coords(float(coords[1]), float(coords[0]))
    return {
        "x1": square_coords["x1"], "y1": square_coords["y1"],
        "x2": square_coords["x2"], "y2": square_coords["y2"],
        "x3": square_coords["x3"], "y3": square_coords["y3"],
        "x4": square_coords["x4"], "y4": square_coords["y4"],
        "individuals": float(data[6]), # from ind
        "households" : float(data[7]) # from men
    }

i = 0
with open(BASE_PATH+'/carreaux_200m_SaintDenis_wgs84.json', 'w') as dest_file:
    dest_file.write('[')
    with open(BASE_PATH+'/carreaux_200m_SaintDenis_wgs84.csv', 'r') as src_file:
        src_file.readline() # skip the header
        line = src_file.readline()
        while line is not None and line != '':
            data = convert_csv_line_to_json_object(line)
            result.append(data)
            dest_file.write(json.dumps(data) + ',\n')
            line = src_file.readline()
            i+=1
            if i % 100 == 0:
                print(f'{i/4230 * 100} %')
        dest_file.write(']')
    debug_squares()
