from datetime import datetime, timedelta
import plotly.graph_objs as go
from static.run import main
from fix import fixer
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('firstlast',
                       help='Choose time for rendering by typing "-firstlast" followed by '
                            '"yyyy-mm-dd hh:mm:ss", for both first = beginning and last = ending',
                       type=str,
                       nargs=4)

my_parser.add_argument('-ns',
                       help='Choose one or more NameServers to visualize by typing "-ns" followed by wanted'
                            ' nameservers like this: "letter".ns.se"4/6", default is "all4" which means '
                            'every nameserver for IPv4',
                       type=str,
                       nargs='*',
                       default='all4')
my_parser.add_argument('-interval',
                       help='choose time difference for measurement results, default is 10 min',
                       type=int,
                       nargs=1,
                       default=[10])
args = my_parser.parse_args()
nameserver = args.ns
firstlast = args.firstlast
interval = args.interval
start = datetime.strptime(firstlast[0] + ' ' + firstlast[1], '%Y-%m-%d %H:%M:%S')
last = datetime.strptime(firstlast[2] + ' ' + firstlast[3], '%Y-%m-%d %H:%M:%S')

print('Interval: ' + str(interval[0]))
print('Initial start time: ' + str(start))
print('Process will stop when start is equal to: ' + str(last))
print('Rendering: ' + str(nameserver))

ms_id = {}
y_dict = {}
x = []

if nameserver is 'all4':
    with open('msmIDs-20191119-to-20191126', 'r') as file:
        f = file.readlines()
        for item in f:
            item = item.rstrip().split(', ')
            ip = int(item[1][-1])
            if ip == 6:
                break
            ms_id[item[1]] = item[0]
    file.close()
else:
    with open('msmIDs-20191119-to-20191126', 'r') as file:
        f = file.readlines()
        for item in f:
            item = item.rstrip().split(', ')
            for numb in range(len(nameserver)):
                if nameserver[numb] == item[1]:
                    ms_id[item[1]] = item[0]
    file.close()

for num in range(1, len(ms_id)+1):  # the amount of y keys in 'data' should be the same as the amount of keys in 'ms_id'
    y_dict['y' + str(num)] = []

while start != last:  # depending on time and interval

    start = start + timedelta(minutes=interval[0])  # interval
    stop = start + timedelta(minutes=10)
    mean_rtt_list = main(start, stop, ms_id)

    for y in y_dict:
        y_dict[y].append(mean_rtt_list[int(y.strip('y'))-1])

    x.append(str(start))

fig = go.Figure()
for y in y_dict:
    name = list(ms_id)[int(y.strip('y'))-1]

    fig.add_trace(go.Scatter(x=x, y=y_dict[y],
                             mode='lines',
                             name=name,
                             hoverinfo='text+y+name',
                             hovertemplate='RTT: %{y}'))


fig.update_layout(title='Median RTT (in milliseconds) for .se NameServers between ' + str(start).split(' ')[0] + 'and ' + str(last).split(' ')[0],
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









