from datetime import datetime, timedelta
import plotly.graph_objs as go
from Static.run import main
from Static.fix import fixer, meta_fixer
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
numberofintervals = args.numberofintervals
interval = args.interval
start = datetime.strptime(first[0] + ' ' + first[1], '%Y-%m-%d %H:%M:%S')
last = start + timedelta(minutes=interval[0]*numberofintervals[0])

print('\nInterval: ' + str(interval[0]))
print('Initial start time: ' + str(start))
print('Process will stop when start is equal to: ' + str(last))
print('Rendering: ' + str(nameserver)+'\n')

ms_id = {}
with open('Files/'+'msmIDs-20191119-to-20191126', 'r') as file:  # change in regards to which week is to be examined
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
    y_dict['y' + str(num)] = []
    x_dict['x' + str(num)] = []

maximum = 0
print('Fetching result from ripeatlas every ' + str(interval) + ' minutes...\n')
while start != last:  # depending on time and interval
    start = start + timedelta(minutes=interval[0])  # interval
    stop = start + timedelta(minutes=10)
    print('Now fetching: '+str(start))
    print('Will stop on: '+str(last)+'\n')

    rtt_list = main(start, stop, ms_id)

    for y in y_dict:
        y_list = []
        x = 'x' + y.strip('y')
        for item in rtt_list[int(y.strip('y'))-1]:
            y_list.append(item)
            x_dict[x].append(start)
        if max(y_list) > maximum:
            maximum = max(y_list)
        y_dict[y].append(y_list)

maximum = [0 - maximum*0.05, maximum + maximum*0.05]
for number in range(1, len(y_dict)+1):
    scatter_y = []
    scatter_x = []
    line_x = []
    line_y = []
    for num in range(0, len(y_dict['y' + str(number)])):
        y = y_dict['y'+str(number)][num]
        x = list(dict.fromkeys(x_dict['x'+str(number)]))[num]

        line_y.append(np.mean(y))
        line_x.append(x)

        x_list = []
        for every_item in y:
            x_list.append(x)

        scatter_x.extend(x_list)
        scatter_y.extend(y)

    data = [go.Scatter(x=scatter_x,
                       y=scatter_y,
                       hoverinfo='text+y+name',
                       hovertemplate='RTT: %{y}',
                       mode='markers',
                       marker_color='#0000FF',
                       opacity=0.6,
                       name='All rtt values'),

            go.Scatter(x=line_x,
                       y=line_y,
                       hoverinfo='text+y+name',
                       hovertemplate='RTT: %{y}',
                       mode='lines',
                       line_color='#FF8000',
                       name='Median rtt based on the same values')]

    fig = go.Figure(data=data)
    if str(first[0]) == str(last).split(' ')[0]:
        title_thing = ' on ' + str(first[0])
    else:
        title_thing = ' between ' + str(first[0]) + ' and ' + str(last).split(' ')[0]
    fig.update_layout(title=list(ms_id)[number-1] + title_thing,
                      yaxis_zeroline=False,
                      xaxis_zeroline=False)
    fig.update_yaxes(range=maximum)
    fig.show()

fixer()
meta_fixer()
