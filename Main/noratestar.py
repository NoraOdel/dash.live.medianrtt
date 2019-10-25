import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly
import sys
import plotly.graph_objs as go
sys.path.append('../')
from Main.run import main
import os

ms =['a', 'b', 'c']
data = {
        'x': [],
        'y1': [],
        'y2': [],
        'y3': []
}

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1('Great Stuff 1 2 3'),
    html.Button('Submit', id='button'),
    html.Div(id='button-basic',
             children='Click to initialize example plot'),
    dcc.Graph(id='example'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 3000,  # in milliseconds, not under 3000 ms --> to fast
        n_intervals=0
    )]
)


@app.callback(Output(component_id='example', component_property='figure'),
              [Input(component_id='interval-component', component_property='n_intervals')])
def update(step):

    rtt_list = main()
    if len(data['x']) == 100:
        for val in data.values():
            val.pop(0)

    fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)

    data['x'].append(step)
    for x in range(1, len(data)):

        data['y'+str(x)].append(rtt_list[x-1])
        fig.append_trace({
            'x': data['x'],
            'y': data['y'+str(x)],
            'name': ms[x-1]+'.ns.se IPv4',
            'mode': 'lines',
            'type': 'scatter'
        }, 1, 1)

    if data['x'][0] != 0:
        for val in data.values():
            val.pop(0)

    for file in os.listdir():
        if 'atlas-results.csv' in file:
            os.remove(file)

    print(data)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
