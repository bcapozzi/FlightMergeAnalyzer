from pylab import *

from mpl_toolkits.mplot3d import Axes3D
from pykml import parser
from geo_utils import seg_length
from geo_utils import cross_track_error
from geo_utils import along_segment_distance
from geo_utils import is_projection_within


import csv

def parse(file_name):
    data = []
    with open(file_name, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row[7]:
                continue
            
            sample = {'time': row[0],
                      'latDeg': float(row[1]),
                      'lonDeg': -float(row[2]),
                      'altFeet': row[7]}
            data.append(sample)
            
    links = []
    dstart = 0
    dend = 0
    for i in range(0,size(data)-1):
        p_prev = data[i];
        p_next = data[i+1];
        curr_length = seg_length(p_prev,p_next)
        dend = dstart + curr_length
        link = {'p1':p_prev,'p2':p_next,'dstart': dstart, 'dend': dend}
        links.append(link)
        dstart = dend

    mf_lat = 30.452517
    mf_lon = 95.861817

    # find link that is smallest cross-track distance from meter fix
    # compute distance "along" link to meter fix
    # set this as the reference distance
    closest_link = []
    min_error = 9999999
    mf_distance_along_link = -1
    
    for link in links:
        # is mf "inside" link?
        if (is_projection_within(link,mf_lat,mf_lon)):
            xtrk_error = abs(cross_track_error(link,mf_lat,mf_lon))
            if (xtrk_error < min_error):
                min_error = xtrk_error
                closest_link = link
                mf_distance_along_link = along_segment_distance(link,mf_lat,mf_lon)


    dref = closest_link['dstart'] + mf_distance_along_link
    for link in links:
        link['dstart_togo'] = link['dstart']-dref
        link['dend_togo'] = link['dend']-dref
        
    return links, closest_link, mf_distance_along_link





