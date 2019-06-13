import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import numpy as np
import statistics
import math


def float_values(trips):
    for trip in trips:
        for key, value in trip.items():
            trip[key] = float(value)                         
    return trips

def parse_trips(trips):
    parsedtrips=[]
    for trip in trips:
        trimtrip=trip.copy()
        
        for key in trip:
            if key != 'trip_distance' and key!= 'pickup_latitude' and key != 'pickup_longitude':
                trimtrip.pop(key)
                
        parsedtrips.append(trimtrip)
    
    return parsedtrips
cleaned_trips = float_values(parsed_trips)

def location(trip):
    loc=[trip['pickup_latitude'], trip['pickup_longitude']]
    return loc

def distance_location(selected_trip, neighbor_trip):
    x=location(selected_trip)
    y=location(neighbor_trip)
    dist=pow((pow(x[0]-y[0],2)+pow(x[1]-y[1],2)) ,.5)
    return dist

def distance_between_neighbors(selected_trip, neighbor_trip):
    neighbor_trip['distance_from_selected']=distance_location(selected_trip, neighbor_trip)
    return neighbor_trip

def distance_all(selected_individual, neighbors):
    alldist=list(map(lambda x : distance_between_neighbors(selected_individual,x),neighbors))
    return alldist

def nearest_neighbors(selected_trip, trips, number = 3):
    sortlist= sorted(distance_all(selected_trip, trips),key = lambda neighbor: neighbor['distance_from_selected'])
    if sortlist[0]['distance_from_selected']==0:
        sortlist.pop(0)
    return sortlist[:number]

def mean_distance(neighbors):
    nearest_distances = list(map(lambda neighbor: neighbor['trip_distance'], neighbors))
    return statistics.mean(nearest_distances)

def zvalue(x,y):
    trip=dict(pickup_latitude=x, pickup_longitude=y)
    nearest_7_neighbors = nearest_neighbors(trip, cleaned_trips or [], number = 7) 
    z=mean_distance(nearest_7_neighbors)
    return z

def deg2num(lat_deg, lon_deg):
    lat_rad = math.radians(lat_deg)
    xtile =(lon_deg + 180.0) / 360.0
    ytile =(1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0
    return [xtile, ytile]

parsed_trips = parse_trips(trips)
cleaned_trips = float_values(parsed_trips)

#40.702030, -74.019704
#40.807611, -73.929674
xminll=40.699984
xmaxll=40.807611
yminll=-74.019704
ymaxll=-73.953073

numpoints=10 #this is the number of x points and y points, so total sample points is this squared
xlist=list(np.linspace(xmin,xmax,numpoints))
ylist=list(np.linspace(ymin,ymax,numpoints))

xx,yy = np.meshgrid(xlist, ylist)
vectorz=np.vectorize(zvalue)
zgrid=vectorz(xx,yy)

mmin=deg2num(xminll,yminll)
mmax=deg2num(xmaxll,ymaxll)

plotx=list(np.linspace(mmin[0],mmax[0],numpoints))
ploty=list(np.linspace(mmin[1],mmax[1],numpoints))
data=[go.Contour(x=plotx,y=ploty,z=zgrid)]
plotly.offline.iplot(data)
