from pykml import parser
from geo_utils import distance
from geo_utils import azimuth
import math


def load_artcc_boundaries():
    with open('artcc.kml') as f:
        doc = parser.parse(f)
        root = doc.getroot()
        boundaries = []
        for child in root.findall('.//{http://earth.google.com/kml/2.2}coordinates'):
            tmp = str(child.text).strip()
            boundaries.append(tmp)


    return boundaries

def convert_to_points(bIn):
    boundary_set = []
    
    for b in bIn:
        boundary = []
        points = b.split(' ')
        if (len(points) < 2):
            continue
        
        #print points
        for p in points:
            vals = p.split(',')
            
            bp = {'lon': -float(vals[0]), 'lat':float(vals[1]), 'alt':float(vals[2])}
            boundary.append(bp)

        boundary_set.append(boundary)

    return boundary_set

def convert_to_xy_boundaries(bIn):

    mf_lat = 30.452517
    mf_lon = 95.861817

    xy_boundaries = []
    
    for b in bIn:
        xy_bndry = []
        for p in b:
            d = distance(mf_lat,mf_lon,p['lat'],p['lon'])
            a = azimuth(mf_lat,mf_lon,p['lat'],p['lon'])
            deast = d*math.sin(a)
            dnorth = d*math.cos(a)
            xy_point = {'x': deast, 'y':dnorth}
            xy_bndry.append(xy_point)

        xy_boundaries.append(xy_bndry)

    return xy_boundaries

def get_boundary_xy(b):
    x = []
    y = []
    for p in b:
        x.append(p['x'])
        y.append(p['y'])

    return x,y
