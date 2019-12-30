'''
Copyright 2019 Nora Odelius odelius.nora@gmail.com
'''

# This program creates a line graph with user defined conditions
# Conditions to be set by the user:
# 1. Starting time (no default value, condition has to be defined)
# 2. Nameservers
# 3. The interval between two fetched measurements
# 4. The amount of measurements to be fetched, ie number of intervals

from datetime import datetime, timedelta
import plotly.graph_objs as go
from Static.run import main
from Static.fix import fixer, meta_fixer, draw
import argparse
import numpy as np
import logging
import chart_studio.plotly as py
import chart_studio.tools as cst

username = 'Noodel'
api_key = 'eOtTbC1LBvxjLyE0JfzA'
cst.set_credentials_file(username=username, api_key=api_key)

with open('Files/'+'logged_messages.log', 'w') as file:
    file.write('This line was written so the previous lines could be deleted\n\n')
logging.basicConfig(filename='Files/'+'logged_messages.log',level=logging.DEBUG)

my_parser = argparse.ArgumentParser()
my_parser.add_argument('first',
                       help='Choose time for rendering by typing'
                            '"yyyy-mm-dd hh:mm:ss"',
                       type=str,
                       nargs=2)
my_parser.add_argument('-numberofintervals',
                       help='Choose how many times results are to be fetched, default is 144. '
                            'If -interval is 10 minutes the timeperiod will be 24h: 144*10 = 1440 minutes --> 24h',
                       type=int,
                       nargs=1,
                       default=[144])
my_parser.add_argument('-ns',
                       help='Choose one or more NameServers to visualize by typing "-ns" followed by wanted'
                            ' nameservers like this: "letter".ns.se"4/6", default is "all4" which means '
                            'every nameserver for IPv4',
                       type=str,
                       nargs='*',
                       default='all')
my_parser.add_argument('-interval',
                       help='choose time difference for measurement results, default is 10 min',
                       type=int,
                       nargs=1,
                       default=[10])

args = my_parser.parse_args()
nameserver = args.ns
first = args.first
interval = args.interval
numberofintervals = args.numberofintervals

start = datetime.strptime(first[0] + ' ' + first[1], '%Y-%m-%d %H:%M:%S')
last = start + timedelta(minutes=interval[0]*numberofintervals[0])

print('\nInterval: ' + str(interval[0]))
print('Initial start time: ' + str(start))
print('Process will stop when start is equal to: ' + str(last))
print('Rendering: ' + str(nameserver)+'\n')


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

y_dict = {}
x_dict = {}
for num in range(1, len(ms_id)+1):  # the amount of y keys in 'data' should be the same as the amount of keys in 'ms_id'
    x_dict['x' + str(num)] = []
    y_dict['y' + str(num)] = []

while start != last:  # depending on time and interval

    start = start + timedelta(minutes=interval[0])  # interval
    stop = start + timedelta(minutes=10)
    print('Now fetching: '+str(start))
    print('Will stop on: '+str(last)+'\n')

    rtt_list = main(start, stop, ms_id)


    for y in y_dict:
        x = 'x' + y.strip('y')
        y_dict[y].append(np.mean(rtt_list[int(y.strip('y'))-1]))
        x_dict[x].append(str(start))

fig = go.Figure()
for y in y_dict:
    name = list(ms_id)[int(y.strip('y'))-1]
    x = 'x' + y.strip('y')
    if int(y.strip('y')) >= 11:
        line_ip = 'lines+markers'
    else:
        line_ip = 'lines'

    fig.add_trace(go.Scatter(x=x_dict[x], y=y_dict[y],
                             mode=line_ip,
                             name=name,
                             hoverinfo='text+y+name',
                             hovertemplate='RTT: %{y}'))

initial = datetime.strptime(first[0], '%Y-%m-%d')
if str(initial).split(' ')[0] == str(last).split(' ')[0]:
    title_part = 'on <br />' + str(initial).split(' ')[0]
else:
    title_part = 'between <br />' + str(initial).split(' ')[0] + ' and ' + str(last).split(' ')[0]
fig.update_layout(title='Median RTT for .se NameServers ' + title_part,
                  yaxis=dict(
                      ticksuffix='ms'
                  ),
                  xaxis=dict(
                      tickmode='auto',
                      nticks=6,
                      dtick=1
                  ))

py.plot(fig, filename='Line graph', auto_open=True)

fixer()
meta_fixer()
draw()
