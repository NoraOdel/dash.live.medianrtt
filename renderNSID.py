'''
Copyright 2019 Nora Odelius odelius.nora@gmail.com
'''

from Static.runNSID import main
from datetime import datetime, timedelta
from Static.fix import fixer, meta_fixer
import plotly.graph_objs as go
import argparse
import numpy as np
import logging

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
x_dict = {'x': []}
for num in range(1, len(ms_id)+1):  # the amount of y keys in 'data' should be the same as the amount of keys in 'ms_id'
    y_dict['y' + str(num)] = []


while start != last:
    temp_y_dict = {}
    start = start + timedelta(minutes=interval[0])
    stop = start + timedelta(minutes=10)
    print('Now fetching: '+str(start))
    print('Will stop on: '+str(last)+'\n')

    stats_csv_list = main(start, stop, ms_id)

    rtt_nsid = []
    for file in stats_csv_list:
        with open('TempFiles/' + file, 'r') as results:
            for row in results:
                if 'ip_dst,proto,rtt,probeID,rcode' in row:
                    continue

                sp = row.split(',')
                rtt = sp[3]
                nsid = sp[8]

                if rtt != '' and nsid != '':
                    rtt = float(rtt)
                    rtt_nsid.append((nsid, rtt))

            if len(rtt_nsid) == 0:
                rtt_nsid.append((0, 0))
        results.close()

    for tuples in rtt_nsid:
        if tuples[0] not in temp_y_dict:
            temp_y_dict[tuples[0]] = [tuples[1]]
        else:
            temp_y_dict[tuples[0]].append(tuples[1])

    for key in temp_y_dict:
        if key not in y_dict:
            y_dict[key] = []
            y_dict[key].append(temp_y_dict[key])
        else:
            y_dict[key].append(temp_y_dict[key])

    x_dict['x'].append(str(start))

fig = go.Figure()
for y in y_dict:

    rtt_mean = []
    for lists in y_dict[y]:
        mean = np.mean(lists)
        rtt_mean.append(mean)
    fig.add_trace(go.Scatter(x=x_dict['x'], y=rtt_mean,
                             mode='lines',
                             name=y,
                             hoverinfo='text+y+name',
                             hovertemplate='RTT: %{y}'))

if str(first[0]) == str(last).split(' ')[0]:
    title_thing = ' on ' + str(first[0])
else:
    title_thing = ' between ' + str(first[0]) + ' and ' + str(last).split(' ')[0]
fig.update_layout(title='Median RTT (in milliseconds) based on NSID ' + title_thing,
                  yaxis=dict(
                      ticksuffix='ms'
                  ),
                  xaxis=dict(
                      tickmode='auto',
                      nticks=6,
                      dtick=1
                  ))
fig.show()

fixer()
meta_fixer()
