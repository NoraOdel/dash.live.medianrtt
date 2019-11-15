import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly
import webbrowser
from datetime import datetime, timedelta
from static.run import main
from static.fix import fixer

data = {  # the amount of y keys in data should be the same as the amount of keys in ms_id dict
        'x': [],
        'datetime': [],
        'y1': []
}


app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(""),
    dcc.Graph(id='example'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 6000,  # in milliseconds, not under 3000 ms --> to fast
        n_intervals=0)])

@app.callback(Output(component_id='example', component_property='figure'),
              [Input(component_id='interval-component', component_property='n_intervals')])
def update(step):
    ms_id = {
        'a.ns.se': '23191329'}  # choose which measurement you'll want to include, and you're DONE!

    start = datetime.utcnow()
    stop = start + timedelta(minutes=10)

    rtt_list = main(start, stop, ms_id)
    if len(data['x']) == 1200:  # when the graph has 1200 coordinates the first one in every list will be removed
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

        data['y'+str(x)].append(rtt_list[x-1])
        fig.append_trace({
            'x': data['datetime'],
            'y': data['y'+str(x)],
            'name': list(ms_id.keys())[x-1],
            'mode': 'lines',
            'type': 'scatter',
            'hovertext': '',
            'hoverinfo': 'text+y+name',
            'hovertemplate': 'RTT: %{y}',
            'opacity': 0.9
        }, 1, 1)

    fig.update_yaxes(ticksuffix="ms")
    fig.update_xaxes(
        tickmode='auto',
        nticks=6,
        dtick=1)

    if data['x'][0] != 0 and data['x'][1] != 1:
        for val in data.values():
            val.pop(0)

    fixer()
    return fig


if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:8050/')
    app.run_server(debug=True)



