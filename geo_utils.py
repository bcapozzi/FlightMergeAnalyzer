from math import *

def to_radians(deg):
    return deg*pi/180.0

def distance(lat1Deg,lon1Deg,lat2Deg,lon2Deg):

    lat1 = to_radians(lat1Deg);
    lon1 = to_radians(lon1Deg);
    lat2 = to_radians(lat2Deg);
    lon2 = to_radians(lon2Deg);

    term1 = (sin((lat1 - lat2) / 2));
    term2 = (sin((lon1 - lon2) / 2));
    d_rad = 2 * asin(sqrt(term1 * term1 + cos(lat1) *
        cos(lat2) * term2 * term2));

    d_nmi = (d_rad * 180.0 / pi * 60.0);
    return d_nmi

def mod(y, x):
    return (y - x * floor(y / x))
    
def azimuth(lat1Deg, lon1Deg, lat2Deg, lon2Deg):

    lat1 = to_radians(lat1Deg);
    lon1 = to_radians(lon1Deg);
    lat2 = to_radians(lat2Deg);
    lon2 = to_radians(lon2Deg);

    tc1 = mod(atan2(sin(lon1 - lon2) * cos(lat2), 
                        cos(lat1) *
                        sin(lat2) -
                        sin(lat1) *
                        cos(lat2) *
                        cos(lon1 - lon2)), 2 * pi)

    if (tc1 > pi):
        tc1 = tc1 - 2*pi
    if (tc1 < -pi):
        tc1 = tc1 + 2*pi
        
    return tc1

def seg_length(p1,p2):
    lat1 = p1['latDeg'] + 0.
    lon1 = p1['lonDeg'] + 0.
    lat2 = p2['latDeg'] + 0.
    lon2 = p2['lonDeg'] + 0.
    return distance(lat1,lon1,lat2,lon2)

def limit(angleIn):
    if (angleIn > pi):
        return angleIn - 2*pi

    if (angleIn < pi):
        return angleIn + 2*pi

    return angleIn
    
def cross_track_error(link,latDeg,lonDeg):

    dToPoint = distance(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)
    aToPoint = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)

    heading = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],
                      link['p2']['latDeg'],link['p2']['lonDeg'])

    relHeading = limit(aToPoint - heading)
    
    term2 = sin(relHeading)
    term1 = sin(dToPoint/3443.91847); 
        
    crossTrackRadians = asin(term1*term2);
    return crossTrackRadians*3443.91847


def along_segment_distance(link, latDeg, lonDeg):
    dToPoint = distance(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)
    aToPoint = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)

    heading = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],
                      link['p2']['latDeg'],link['p2']['lonDeg'])

    relHeading = limit(aToPoint - heading)
        
    return dToPoint*cos(relHeading);
        
def is_projection_within(link, latDeg, lonDeg):
    d = along_segment_distance(link, latDeg, lonDeg);
    return d > 0 and d <= seg_length(link['p1'],link['p2'])


