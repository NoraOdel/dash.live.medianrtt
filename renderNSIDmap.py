'''
Copyright 2019 Nora Odelius odelius.nora@gmail.com
'''

import pandas as pd
import plotly.express as px
import argparse
from datetime import timedelta, datetime
from Static.runNSID import main
from Static.fix import fixer, meta_fixer

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-start',
                       help='Choose time for measurements initiation by typing "-time" followed by '
                            '"yyyy-mm-dd hh:mm:ss", default is current utc time',
                       type=str,
                       nargs=2,
                       default='now')
my_parser.add_argument('-ns',
                       help='Choose one or more NameServers to visualize by typing "-ns" followed by wanted'
                            ' nameservers, default is a4 which equals to a.ns.se IPv4',
                       type=str,
                       nargs='*',
                       default='a.ns.se4'.split())

args = my_parser.parse_args()
first = args.start
nameserver = args.ns
start = datetime.strptime(first[0] + ' ' + first[1], '%Y-%m-%d %H:%M:%S')
stop = start + timedelta(minutes=10)

ms_id = {}
with open('Files/msmIDs-20191119-to-20191126', 'r') as file:  # change in regards to which week is to be examined
    f = file.readlines()
    for item in f:
        item = item.rstrip().split(', ')
        if nameserver is 'all':
            ip = int(item[1][-1])
            ms_id[item[1]] = item[0]
        else:
            for num in range(len(nameserver)):
                if nameserver[num] == item[1]:
                    ms_id[item[1]] = item[0]
file.close()

stats_list = main(start, stop, ms_id)

for results in stats_list:

    sweden_coordinates = pd.read_csv('TempFiles/' + results).dropna()
    high_vals = sweden_coordinates.loc[sweden_coordinates['rtt'] > 500]
    high_vals['Extreme values'] = 'Extreme Values'

    indexNames = sweden_coordinates[sweden_coordinates['rtt'] > 500].index
    sweden_coordinates.drop(indexNames, inplace=True)

    fig = px.scatter_mapbox(sweden_coordinates,
                            lat="latitud",
                            lon="longitud",
                            color='nsid',
                            zoom=3,
                            height=500,
                            opacity=1,
                            size='rtt')
    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox_layers=[
            {
                "sourcetype": "raster",
                "source": ["https://geo.weather.gc.ca/geomet/?"
                           "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                           "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
            },
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
          ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      title=dict(text="A Chart"))
    fig.show()

fixer()
meta_fixer()