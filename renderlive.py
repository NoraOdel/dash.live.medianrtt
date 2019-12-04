import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly
import webbrowser
from datetime import datetime, timedelta
from Static.run import main
from Static.fix import fixer, meta_fixer
import argparse
import numpy as np
import logging

with open('Files/'+'logged_messages.log', 'w') as file:
    file.write('This line was written so the previous lines could be deleted\n\n')
logging.basicConfig(filename='Files/'+'logged_messages.log',level=logging.DEBUG)

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-ns',
                       help='Choose one or more NameServers to visualize by typing "-ns" followed by wanted'
                            ' nameservers like this: "letter".ns.se"4/6", default is "all4" which '
                            'equals to every nameserver for IPv4',
                       type=str,
                       nargs='*',
                       default='all4')
args = my_parser.parse_args()
nameserver = args.ns


data = {  # the amount of y keys in data should be the same as the amount of keys in ms_id dict
        'x': [],
        'datetime': []
}
ms_id = {}

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(""),
    dcc.Graph(id='example'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 10000,  # in milliseconds, not under 3000 ms --> to fast
        n_intervals=0)])

if nameserver is 'all4':
    with open('msmIDs-20191119-to-20191126', 'r') as file:  # change in regards to which week is to be examined
        f = file.readlines()
        for item in f:
            item = item.rstrip().split(', ')
            ip = int(item[1][-1])
            if ip == 6:
                break
            ms_id[item[1]] = item[0]
    file.close()
elif nameserver == 'all':
    with open('msmIDs-20191119-to-20191126', 'r') as file:  # change in regards to which week is to be examined
        f = file.readlines()
        for item in f:
            item = item.rstrip().split(', ')
            ip = int(item[1][-1])
            ms_id[item[1]] = item[0]
    file.close()
else:
    with open('msmIDs-20191119-to-20191126', 'r') as file:  # change in regards to which week is to be examined
        f = file.readlines()
        for item in f:
            item = item.rstrip().split(', ')
            for num in range(len(nameserver)):
                if nameserver[num] == item[1]:
                    ms_id[item[1]] = item[0]
    file.close()

for num in range(1, len(ms_id)+1):  # the amount of y keys in 'data' should be the same as the amount of keys in 'ms_id'
    data['y' + str(num)] = []

print(data)

@app.callback(Output(component_id='example', component_property='figure'),
              [Input(component_id='interval-component', component_property='n_intervals')])
def update(step):

    start = datetime.utcnow()
    stop = start + timedelta(minutes=10)
    print('Now fetching: '+str(start))
    print('Will stop on: '+str(last)+'\n')

    rtt_list = main(start, stop, ms_id)
    if len(data['x']) == 200:  # when the graph has 1200 coordinates the first one in every list will be removed
        for val in data.values():
            val.pop(0)

    fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig.layout = dict(
        title=dict(
            xanchor='left',
            text='Median RTT (in milliseconds) for .se NameServers'
        ),
        showlegend=True,
        autosize=True,
        xaxis=dict(
            ticks="outside",
            tickangle=-45),
        yaxis=dict(
            ticks="outside")
    )

    data['x'].append(step)
    data['datetime'].append(str(datetime.now().strftime('%H:%M:%S')))
    print(step)
    for x in range(1, len(ms_id) + 1):

        data['y'+str(x)].append(np.mean(rtt_list[x-1]))
        fig.append_trace({
            'x': data['datetime'],
            'y': data['y'+str(x)],
            'name': list(ms_id.keys())[x-1],
            'mode': 'lines',
            'type': 'scatter',
            'hoverinfo': 'text+y+name',
            'hovertemplate': 'RTT: %{y}',
            'opacity': 0.9
        }, 1, 1)

    fig.update_yaxes(ticksuffix="ms")
    fig.update_xaxes(
        tickmode='auto',
        nticks=6,
        dtick=1)
    print(data)

    if data['x'][0] != 0 and data['x'][1] != 1:
        for vals in data.values():
            vals.pop(0)

    fixer()
    return fig


if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:8050/')
    app.run_server(debug=True)
    meta_fixer()




