from datetime import datetime, timedelta
import plotly.graph_objs as go
from static.run import main
from static.fix import fixer

y_dict = {'y1': []}  # the amount of y keys in 'data' should be the same as the amount of keys in 'ms_id' dict
x = []

last = datetime.utcnow()
start = last - timedelta(hours=5)  # time
step = 0
while start != last:  # depending on time and interval
    start += timedelta(minutes=30*step)  # interval
    stop = start + timedelta(minutes=10)

    ms_id = {
        'a.ns.se': '23191329'}  # choose which measurement you'll want to include, and you're DONE!

    mean_rtt_list = main(start, stop, ms_id)

    for y in y_dict:
        y_dict[y].append(mean_rtt_list[int(y[1])-1])

    x.append(str(start))
    step += 1

fig = go.Figure()
for y in y_dict:
    fig.add_trace(go.Scatter(x=x, y=y_dict[y],
                             mode='lines',
                             name=y,
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









