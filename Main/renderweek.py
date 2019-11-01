from datetime import datetime, timedelta
import plotly.graph_objs as go
import sys
sys.path.append('../')
from Main.run import main

y1 = []
y2 = []
x = []

first = datetime.strptime('2019-10-20 00:00:00', '%Y-%m-%d %H:%M:%S')
last = first + timedelta(weeks=1)
for step in range(0, 85):
    print(step)
    start = first + timedelta(hours=2*step)
    stop = start + timedelta(minutes=10)
    mean_rtt_list = main(start, stop)

    y1.append(mean_rtt_list[0])
    y2.append(mean_rtt_list[1])
    x.append(str(start))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1,
                         mode='lines',
                         name='a.ns.se',
                         hoverinfo='text+y+name',
                         hovertemplate='RTT: %{y}'))
fig.add_trace(go.Scatter(x=x, y=y2,
                         mode='lines',
                         name='b.ns.se',
                         hoverinfo='text+y+name',
                         hovertemplate='RTT: %{y}'))

fig.update_layout(title='Median RTT (in milliseconds) for a.ns.se and b.ns.se IPv4 between ' + str(first).split(' ')[0] + ' and ' + str(last).split(' ')[0],
                  yaxis=dict(
                      ticksuffix='ms'
                  ),
                  xaxis=dict(
                      tickmode='auto',
                      nticks=9,
                      dtick=1
                  ))
fig.show()










