import plotly
import plotly.graph_objs as go
import numpy as np

import statistics
def mean_distance(neighbors):
    nearest_distances = list(map(lambda neighbor: neighbor['trip_distance'], neighbors))
    return statistics.mean(nearest_distances)
def zvalue(x,y):
    trip=dict(pickup_latitude=x, pickup_longitude=y)
    nearest_7_neighbors = nearest_neighbors(trip, cleaned_trips or [], number = 7) 
    z=mean_distance(nearest_7_neighbors)
    return z
    
#40.702030, -74.019704
#40.807611, -73.929674
xmin=40.699984
xmax=40.807611
ymin=-74.019704
ymax=-73.953073
numpoints=10 #this is the number of x points and y points, so total sample points is this squared
xlist=list(np.linspace(xmin,xmax,numpoints))
ylist=list(np.linspace(ymin,ymax,numpoints))

xx,yy = np.meshgrid(xlist, ylist)
vectorz=np.vectorize(zvalue)
zgrid=vectorz(xx,yy)
data=[go.Contour(x=xlist,y=ylist,z=zgrid)]
