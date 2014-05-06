from pylab import *

from mpl_toolkits.mplot3d import Axes3D
from pykml import parser
import csv

def to_radians(deg):
    return deg*math.pi/180.0

def distance(lat1Deg,lon1Deg,lat2Deg,lon2Deg):

    lat1 = to_radians(lat1Deg);
    lon1 = to_radians(lon1Deg);
    lat2 = to_radians(lat2Deg);
    lon2 = to_radians(lon2Deg);

    term1 = (math.sin((lat1 - lat2) / 2));
    term2 = (math.sin((lon1 - lon2) / 2));
    d_rad = 2 * math.asin(math.sqrt(term1 * term1 + math.cos(lat1) *
        math.cos(lat2) * term2 * term2));

    d_nmi = (d_rad * 180.0 / math.pi * 60.0);
    return d_nmi

def mod(y, x):
    return (y - x * math.floor(y / x))
    
def azimuth(lat1Deg, lon1Deg, lat2Deg, lon2Deg):

    lat1 = to_radians(lat1Deg);
    lon1 = to_radians(lon1Deg);
    lat2 = to_radians(lat2Deg);
    lon2 = to_radians(lon2Deg);

    tc1 = mod(math.atan2(math.sin(lon1 - lon2) * math.cos(lat2), 
                        math.cos(lat1) *
                        math.sin(lat2) -
                        math.sin(lat1) *
                        math.cos(lat2) *
                        math.cos(lon1 - lon2)), 2 * math.pi)

    if (tc1 > math.pi):
        tc1 = tc1 - 2*math.pi
    if (tc1 < -math.pi):
        tc1 = tc1 + 2*math.pi
        
    return tc1

def seg_length(p1,p2):
    lat1 = p1['latDeg'] + 0.
    lon1 = p1['lonDeg'] + 0.
    lat2 = p2['latDeg'] + 0.
    lon2 = p2['lonDeg'] + 0.
    return distance(lat1,lon1,lat2,lon2)

def limit(angleIn):
    if (angleIn > math.pi):
        return angleIn - 2*math.pi

    if (angleIn < math.pi):
        return angleIn + 2*math.pi

    return angleIn
    
def cross_track_error(link,latDeg,lonDeg):

    dToPoint = distance(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)
    aToPoint = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)

    heading = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],
                      link['p2']['latDeg'],link['p2']['lonDeg'])

    relHeading = limit(aToPoint - heading)
    
    term2 = math.sin(relHeading)
    term1 = math.sin(dToPoint/3443.91847); 
        
    crossTrackRadians = math.asin(term1*term2);
    return crossTrackRadians*3443.91847


def along_segment_distance(link, latDeg, lonDeg):
    dToPoint = distance(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)
    aToPoint = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],latDeg,lonDeg)

    heading = azimuth(link['p1']['latDeg'],link['p1']['lonDeg'],
                      link['p2']['latDeg'],link['p2']['lonDeg'])

    relHeading = limit(aToPoint - heading)
        
    return dToPoint*math.cos(relHeading);
        
def is_projection_within(link, latDeg, lonDeg):
    d = along_segment_distance(link, latDeg, lonDeg);
    return d > 0 and d <= seg_length(link['p1'],link['p2'])

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

b = load_artcc_boundaries()
pb = convert_to_points(b)
bxy = convert_to_xy_boundaries(pb)

        

links1,c1,dref1 = parse('asq4710.csv')
links2,c2,dref2 = parse('skw4490.csv')

p1 = get_points(links1)
p2 = get_points(links2)

x1,y1,z1 = to_xyz_points(p1)
x2,y2,z2 = to_xyz_points(p2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(len(x1)):
    ax.plot([x1[i],x1[i]],[y1[i],y1[i]],[0.0, z1[i]], color='b', alpha=0.3)
    
ax.plot(x1,y1,z1,'o', markersize=8, markerfacecolor='b', color='b')

for i in range(len(x2)):
    ax.plot([x2[i],x2[i]],[y2[i],y2[i]],[0.0, z2[i]], color='r', alpha=0.3)

ax.plot(x2,y2,z2,'o', markersize=8, markerfacecolor='r', color='r')

ax.plot(x1,y1,0,color='b')
ax.plot(x2,y2,0,color='r')

for bd in bxy:
    bx,by = get_boundary_xy(bd)
    ax.plot(bx,by,0,color='0.6')
    
ax.set_xlabel('east (nmi), from MF')
ax.set_ylabel('north (nmi), from MF')
ax.set_zlabel('up (feet)')
ax.set_xlim([-200,1000])
ax.set_ylim([-200,1000])

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

dx1,dy1 = toXY(links1)
dx2,dy2 = toXY(links2)

ax2.plot(dx1,dy1,color='b')
ax2.plot(dx2,dy2,color='r')
ax2.set_xlabel('distance to MF, nmi')
ax2.set_ylabel('altitude (feet)')

show()


#n = 256
#X = np.linspace(-np.pi,np.pi,n,endpoint=True)
#Y = np.sin(2*X)

#plot (X, Y+1, color='blue', alpha=1.00)
#fill_between(X, 1, Y+1, color='blue', alpha=.25)

#plot (X, Y-1, color='blue', alpha=1.00)
#fill_between(X, -1, Y-1, (Y-1) > -1, color='blue', alpha=.25)
#fill_between(X, -1, Y-1, (Y-1) < -1, color='red',  alpha=.25)

#plot (X, Y+1, color='blue', alpha=1.00)
#plot (X, Y-1, color='blue', alpha=1.00)
#show()
