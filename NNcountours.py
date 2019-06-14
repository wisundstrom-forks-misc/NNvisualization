!pip install plotly
import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import numpy as np
import statistics
import math
from folium import plugins
from scipy.ndimage import imread

import json
# First, read the file
trips_file = open('trips.json')
# Then, convert contents to list of dictionaries 
trips = json.load(trips_file)
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

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile =(lon_deg + 180.0) / 360.0*n
    ytile =(1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0*n
    return [xtile, ytile]
    
    parsed_trips = parse_trips(trips)
cleaned_trips = float_values(parsed_trips)




xminll=40.701030
xmaxll=40.816453
yminll=-74.029704
ymaxll=-73.921881

xbr=40.708998
ybr=-73.974842
xtl=40.816453
ytl=-73.968224

numpoints=50 #this is the number of x points and y points, so total sample points is this squared
xlist=list(np.linspace(xminll,xmaxll,numpoints))
ylist=list(np.linspace(yminll,ymaxll,numpoints))

xx,yy = np.meshgrid(xlist, ylist)
vectorz=np.vectorize(zvalue)
zgrid=vectorz(xx,yy)

import folium
import os


marker = folium.CircleMarker(location = [xminll, yminll], radius=10)
marker2 = folium.CircleMarker(location = [xmaxll, ymaxll], radius=10)
marker3 = folium.CircleMarker(location = [xbr, ybr], radius=10)
marker4 = folium.CircleMarker(location = [xtl, ytl], radius=10)

manhattan_map = folium.Map(location=[40.7589, -73.9851], zoom_start=12)
marker.add_to(manhattan_map)
marker2.add_to(manhattan_map)
marker3.add_to(manhattan_map)
marker4.add_to(manhattan_map)

manhattan_map

xaxis=dict(
        
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        showticklabels=False)

layout = go.Layout(yaxis=dict(scaleanchor="x", scaleratio=1, showgrid=False,
    zeroline=False,
    showline=False,
    ticks='',
    showticklabels=False),xaxis=xaxis)
    )
layout.update(dict(shapes = [
        {
            'type': 'path',
            'path':f'M {xminll},{yminll} L{xbr},{ybr} L{xmaxll},{ymaxll} L{xtl},{ytl} L{xminll},{yminll}',
            'opacity': 1,
            'line': {
                'width': 2,
                'color':'rgb(29, 240, 4)',
            }
        }]
        ))
data=[go.Contour(x=xlist,y=ylist,z=zgrid, showscale=False, visible=True)]
fig=go.Figure(data=data, layout=layout)
plotly.offline.iplot(fig)


    
    
