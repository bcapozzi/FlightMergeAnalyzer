from geo_utils import distance
from geo_utils import azimuth
import math


def toXY(links):

    x = []
    y = []
    for link in links:
        x.append(link['dstart_togo'])
        altString = link['p1']['altFeet']
        y.append(float(altString.replace(',','')))

    return x,y

def get_points(linksIn):

    p = []
    for link in linksIn:
        p.append(link['p1'])

    return p

def to_xy_points(points):

    x = []
    y = []
    mf_lat = 30.452517
    mf_lon = 95.861817
    for p in points:
        d = distance(mf_lat,mf_lon,p['latDeg'],p['lonDeg'])
        a = azimuth(mf_lat,mf_lon,p['latDeg'],p['lonDeg'])
        deast = d*math.sin(a)
        dnorth = d*math.cos(a)
        x.append(deast)
        y.append(dnorth)

    return x,y
        
        
def to_xyz_points(points):
    x = []
    y = []
    z = []
    mf_lat = 30.452517
    mf_lon = 95.861817
    for p in points:
        d = distance(mf_lat,mf_lon,p['latDeg'],p['lonDeg'])
        a = azimuth(mf_lat,mf_lon,p['latDeg'],p['lonDeg'])
        deast = d*math.sin(a)
        dnorth = d*math.cos(a)
        x.append(deast)
        y.append(dnorth)
        z.append(float(p['altFeet'].replace(',','')))

    return x,y,z


