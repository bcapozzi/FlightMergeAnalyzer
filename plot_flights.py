from pylab import *

from mpl_toolkits.mplot3d import Axes3D
import csv

from nas_data_loader import *
from track_utils import *
from flight_csv_parser import parse


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
