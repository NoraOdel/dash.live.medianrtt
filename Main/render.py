import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly
import sys
sys.path.append('../')
from Main.run import main
import os
import webbrowser

ms = ['a', 'b']
data = {
        'x': [],
        'y1': [],
        'y2': []
}

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(""),
    dcc.Graph(id='example'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 4000,  # in milliseconds, not under 3000 ms --> to fast
        n_intervals=0)]
)

@app.callback(Output(component_id='example', component_property='figure'),
              [Input(component_id='interval-component', component_property='n_intervals')])
def update(step):

    rtt_list = main()
    if len(data['x']) == 500:
        for val in data.values():
            val.pop(0)

    fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig.layout = dict(
        title=dict(
            xanchor='left',
            text='Median RTT (in milliseconds) for .se NameServers'
        ),
        showlegend=True,
        autosize=True
    )

    data['x'].append(step)
    print(step)
    for x in range(1, len(data)):

        data['y'+str(x)].append(rtt_list[x-1])
        print(rtt_list[x-1])
        fig.append_trace({
            'x': data['x'],
            'y': data['y'+str(x)],
            'name': ms[x-1]+'.ns.se IPv4',
            'mode': 'lines',
            'type': 'scatter',
            'hovertext': '',
            'hoverinfo': 'text+y+name',
            'hovertemplate': 'RTT: %{y}',
            'opacity': 0.9
        }, 1, 1)

    if data['x'][0] != 0 and data['x'][1] != 1:
        for val in data.values():
            val.pop(0)

    for file in os.listdir():
        if 'atlas-results.csv' in file:
            os.remove(file)

    return fig


if __name__ == '__main__':

    webbrowser.open_new('http://127.0.0.1:8050/')
    app.run_server(debug=True)

